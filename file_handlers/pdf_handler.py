import re
import io
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, BinaryIO
from datetime import datetime
import tempfile
import os
import warnings

class PDFHandler:
    
    
    def extract_text(self, filepath: str, method: str = None) -> str:
        if method is None:
            for extraction_method in self.extraction_methods:
                try:
                    text = self._extract_with_method(filepath, extraction_method)
                    if text and len(text.strip()) > 0:
                        return text
                except Exception as e:
                    continue
            return self._extract_fallback(filepath)
        else:
            return self._extract_with_method(filepath, method)
    
    def _extract_with_method(self, filepath: str, method: str) -> str:
        cache_key = f"{filepath}_{method}"
        if cache_key in self._extraction_cache:
            return self._extraction_cache[cache_key]
        
        try:
            if method == 'pdfplumber':
                text = self._extract_with_pdfplumber(filepath)
            elif method == 'pypdf':
                text = self._extract_with_pypdf(filepath)
            elif method == 'pdfminer':
                text = self._extract_with_pdfminer(filepath)
            elif method == 'fallback':
                text = self._extract_fallback(filepath)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
            self._extraction_cache[cache_key] = text
            return text
            
        except ImportError:
            raise ImportError(f"Required library for {method} not installed")
        except Exception as e:
            raise Exception(f"Failed to extract text with {method}: {str(e)}")
    
    def _extract_with_pdfplumber(self, filepath: str) -> str:
        import pdfplumber
        
        text_parts = []
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = range(total_pages)
            
            if self.max_pages > 0:
                pages_to_process = range(min(self.max_pages, total_pages))
        for i in pages_to_process:
                page = pdf.pages[i]
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                if self.extract_tables:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            table_text = self._format_table_text(table)
                            if table_text:
                                text_parts.append(table_text)
                if self.extract_images:
                    images = page.images
                    for img in images:
                        if self.ocr_enabled:
                            ocr_text = self._extract_text_from_image(img)
                            if ocr_text:
                                text_parts.append(f"[Image Text: {ocr_text}]")
        
        return '\n'.join(text_parts)
    
    def _extract_with_pypdf(self, filepath: str) -> str:
        from pypdf import PdfReader
        
        text_parts = []
        
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            pages_to_process = range(total_pages)
            
            if self.max_pages > 0:
                pages_to_process = range(min(self.max_pages, total_pages))
            
            for i in pages_to_process:
                page = reader.pages[i]
                page_text = page.extract_text()
                if page_text:
                    page_text = self._clean_pdf_text(page_text)
                    text_parts.append(page_text)
        
        return '\n'.join(text_parts)
    
    def _extract_with_pdfminer(self, filepath: str) -> str:
        from pdfminer.high_level import extract_text
        if self.max_pages > 0:
            text = extract_text(filepath, page_numbers=list(range(self.max_pages)))
        else:
            text = extract_text(filepath)
        
        return self._clean_pdf_text(text)
    
    def _extract_fallback(self, filepath: str) -> str:
        text = ""
        try:
            import subprocess
            result = subprocess.run(
                ['pdftotext', filepath, '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                text = result.stdout
        except:
            pass
        if not text.strip():
            try:
                import subprocess
                result = subprocess.run(
                    ['strings', filepath],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    text = result.stdout
                    lines = text.split('\n')
                    filtered_lines = []
                    for line in lines:
                        for line in lines:
                            if len(line) > 3 and sum(c.isprintable() for c in line) / len(line) > 0.7:
                                filtered_lines.append(line)
                    text = '\n'.join(filtered_lines)
            except:
                pass
        
        return self._clean_pdf_text(text)
    
    def _extract_text_from_image(self, image_data: Any) -> str:
        if not self.ocr_enabled:
            return ""
        try:
            import pytesseract
            from PIL import Image
            if hasattr(image_data, 'to_image'):
                pil_image = image_data.to_image()
            else:
                pil_image = Image.open(io.BytesIO(image_data['stream'].get_data()))
            text = pytesseract.image_to_string(pil_image)
            return text.strip()
        except ImportError:
            return ""
        except Exception as e:
            print(f"Warning: OCR failed: {e}")
            return ""
    
    def _format_table_text(self, table: List[List]) -> str:
        if not table:
            return ""
        formatted_rows = []
        for row in table:
            row_text = ' | '.join(str(cell) if cell is not None else '' for cell in row)
            formatted_rows.append(row_text)
        
        return '\n'.join(formatted_rows)
    
    def _clean_pdf_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)  
        text = re.sub(r'([.,;:!?])\s+', r'\1 ', text)  
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        
        return text.strip()
    
    
    def extract_metadata(self, filepath: str) -> Dict[str, Any]:
        metadata = {
            'filename': Path(filepath).name,
            'file_size': Path(filepath).stat().st_size,
            'modified': datetime.fromtimestamp(Path(filepath).stat().st_mtime).isoformat(),
            'created': datetime.fromtimestamp(Path(filepath).stat().st_ctime).isoformat(),
            'pdf_metadata': {},
            'security': {},
            'pages': 0,
            'is_scanned': False,
            'has_text_layer': True
        }
        try:
            metadata.update(self._extract_metadata_pypdf(filepath))
        except:
            try:
                metadata.update(self._extract_metadata_pdfplumber(filepath))
            except:
                try:
                    metadata.update(self._extract_metadata_pdfminer(filepath))
                except Exception as e:
                    print(f"Warning: Could not extract PDF metadata: {e}")
        metadata['is_scanned'] = self._is_scanned_pdf(filepath)
        metadata['has_text_layer'] = self._has_text_layer(filepath)
        
        return metadata

    def _extract_metadata_pypdf(self, filepath: str) -> Dict[str, Any]:
        from pypdf import PdfReader
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            metadata['pages'] = len(reader.pages)
            if reader.metadata:
                for key, value in reader.metadata.items():
                    if value:
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
            if reader.is_encrypted:
                metadata['security'] = {
                    'encrypted': True,
                    'permissions': {
                        'print': not (reader._encryption.get('/Print') == 'false'),
                        'modify': not (reader._encryption.get('/Modify') == 'false'),
                        'copy': not (reader._encryption.get('/Copy') == 'false'),
                        'annotate': not (reader._encryption.get('/Annotate') == 'false')
                    }
                }
            else:
                metadata['security'] = {'encrypted': False}
        
        return metadata
    
    def _extract_metadata_pdfplumber(self, filepath: str) -> Dict[str, Any]:
        import pdfplumber
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        with pdfplumber.open(filepath) as pdf:
            metadata['pages'] = len(pdf.pages)
            if hasattr(pdf, 'metadata') and pdf.metadata:
                for key, value in pdf.metadata.items():
                    if value:
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
        
        return metadata
    
    def _extract_metadata_pdfminer(self, filepath: str) -> Dict[str, Any]:
        from pdfminer.pdfparser import PDFParser
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.psparser import PSLiteral
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        
        with open(filepath, 'rb') as file:
            parser = PDFParser(file)
            doc = PDFDocument(parser)
            if hasattr(doc, 'catalog'):
                pages_ref = doc.catalog.get('Pages')
                if pages_ref:
                    try:
                        metadata['pages'] = doc.catalog['Pages']['Count']
                    except:
                        pass
            if doc.info:
                for key, value in doc.info[0].items():
                    if value:
                        if isinstance(value, PSLiteral):
                            value = value.name
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
            if doc._security_handler:
                metadata['security'] = {'encrypted': True}
            else:
                metadata['security'] = {'encrypted': False}
        
        return metadata

    def _is_scanned_pdf(self, filepath: str) -> bool:
        try:
            text = self.extract_text(filepath, method='pypdf')
            if not text or len(text.strip()) < 50:
                return True
            from pypdf import PdfReader
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                if reader.pages:
                    page_text = reader.pages[0].extract_text()
                    if page_text and len(page_text.strip()) < 100:
                        return True
            
            return False
        except:
            return True 
    
    def _has_text_layer(self, filepath: str) -> bool:
        try:
            text = self.extract_text(filepath, method='pypdf')
            if text and len(text.strip()) > 100:
                words = text.split()
                if len(words) > 20:
                    alphabetic_words = sum(1 for word in words if word.isalpha())
                    if alphabetic_words / len(words) > 0.5:
                        return True
            
            return False
            
        except:
            return False
    
    def analyze_pdf_structure(self, filepath: str) -> Dict[str, Any]:
        structure = {
            'pages': [],
            'fonts': [],
            'images': [],
            'links': [],
            'annotations': [],
            'form_fields': [],
            'outlines': [],
            'sections': []
        }
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_info = {
                        'page_number': i + 1,
                        'width': page.width,
                        'height': page.height,
                        'rotation': page.rotation,
                        'text_objects': len(page.chars) if hasattr(page, 'chars') else 0,
                        'images': len(page.images) if hasattr(page, 'images') else 0
                    }
                    page_text = page.extract_text()
                    if page_text:
                        words = page_text.split()
                        page_info.update({
                            'char_count': len(page_text),
                            'word_count': len(words),
                            'line_count': page_text.count('\n') + 1,
                            'has_text': True
                        })
                    else:
                        page_info.update({
                            'char_count': 0,
                            'word_count': 0,
                            'line_count': 0,
                            'has_text': False
                        })
                    
                    structure['pages'].append(page_info)
                if hasattr(pdf, 'fonts'):
                    for font_name, font_data in pdf.fonts.items():
                        structure['fonts'].append({
                            'name': font_name,
                            'type': str(type(font_data))
                        })
                total_images = sum(len(page.images) for page in pdf.pages)
                structure['images'] = [{'count': total_images}]
        except Exception as e:
            print(f"Warning: Could not analyze PDF structure with pdfplumber: {e}")
            try:
                from pypdf import PdfReader 
                with open(filepath, 'rb') as file:
                    reader = PdfReader(file)
                    for i, page in enumerate(reader.pages):
                        page_text = page.extract_text()
                        words = page_text.split() if page_text else []
                        page_info = {
                            'page_number': i + 1,
                            'text_objects': 'N/A',
                            'images': 'N/A',
                            'char_count': len(page_text) if page_text else 0,
                            'word_count': len(words),
                            'line_count': page_text.count('\n') + 1 if page_text else 0,
                            'has_text': bool(page_text and page_text.strip())
                        }
                        structure['pages'].append(page_info)
            except Exception as e2:
                print(f"Warning: Could not analyze PDF structure with PyPDF: {e2}")
        
        return structure
    
    def extract_images(self, filepath: str, output_dir: str = None) -> List[Dict[str, Any]]:
        images = []
        
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            import pdfplumber
            from PIL import Image
            
            with pdfplumber.open(filepath) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    for img_num, img in enumerate(page.images):
                        try:
                            img_info = {
                                'page': page_num + 1,
                                'index': img_num,
                                'width': img['width'],
                                'height': img['height'],
                                'name': img.get('name', f'image_{page_num}_{img_num}'),
                                'bpc': img.get('bpc', 8),   
                                'colorspace': img.get('colorspace', 'unknown')
                            }
                            if 'stream' in img:
                                img_data = img['stream'].get_data()
                                img_info['size_bytes'] = len(img_data)
                                if output_dir:
                                    img_filename = f"page_{page_num+1}_img_{img_num}.png"
                                    img_path = Path(output_dir) / img_filename
                                    
                                    try:
                                        pil_image = Image.open(io.BytesIO(img_data))
                                        pil_image.save(img_path)
                                        img_info['saved_path'] = str(img_path)
                                    except Exception as e:
                                        print(f"Warning: Could not save image: {e}")
                                img_hash = hashlib.md5(img_data).hexdigest()
                                img_info['hash'] = img_hash
                            
                            images.append(img_info)
                            
                        except Exception as e:
                            print(f"Warning: Could not extract image {img_num} from page {page_num}: {e}")
        
        except Exception as e:
            print(f"Warning: Could not extract images: {e}")
        
        return images
    
    def extract_tables(self, filepath: str, pages: List[int] = None) -> List[Dict[str, Any]]:
        tables = []
        
        try:
            import pdfplumber
            
            with pdfplumber.open(filepath) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    if pages and (page_num + 1) not in pages:
                        continue
                    
                    page_tables = page.extract_tables()
                    
                    for table_num, table_data in enumerate(page_tables):
                        if table_data:
                            table_info = {
                                'page': page_num + 1,
                                'table_number': table_num + 1,
                                'rows': len(table_data),
                                'columns': len(table_data[0]) if table_data[0] else 0,
                                'data': table_data,
                                'formatted_text': self._format_table_text(table_data)
                            }
                            tables.append(table_info)
        
        except Exception as e:
            print(f"Warning: Could not extract tables: {e}")
        
        return tables
    
    def validate_pdf(self, filepath: str) -> Dict[str, Any]:
        validation = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        try:
            if not Path(filepath).exists():
                validation['errors'].append('File does not exist')
                return validation
            if not filepath.lower().endswith('.pdf'):
                validation['warnings'].append('File extension is not .pdf')
            file_size = Path(filepath).stat().st_size
            validation['file_info']['size_bytes'] = file_size
            
            if file_size == 0:
                validation['errors'].append('File is empty')
                return validation
            with open(filepath, 'rb') as f:
                header = f.read(5)
                if header != b'%PDF-':
                    validation['errors'].append('File is not a valid PDF (wrong header)')
                    return validation
            try:
                from pypdf import PdfReader
                with open(filepath, 'rb') as file:
                    reader = PdfReader(file)
                    num_pages = len(reader.pages)
                    validation['file_info']['pages'] = num_pages
                    
                    if num_pages == 0:
                        validation['errors'].append('PDF has no pages')
                    if reader.is_encrypted:
                        validation['warnings'].append('PDF is encrypted')
                    if num_pages > 0:
                        try:
                            page_text = reader.pages[0].extract_text()
                            if page_text:
                                validation['file_info']['has_text'] = True
                                validation['file_info']['sample_text'] = page_text[:200]
                            else:
                                validation['warnings'].append('First page has no extractable text')
                        except:
                            validation['warnings'].append('Could not extract text from first page')
            
            except Exception as e:
                validation['errors'].append(f'Failed to open PDF with PyPDF: {str(e)}')
                return validation
            self._check_pdf_issues(filepath, validation)
            validation['is_valid'] = len(validation['errors']) == 0
        except Exception as e:
            validation['errors'].append(f'Validation failed: {str(e)}')
        
        return validation
    
    def _check_pdf_issues(self, filepath: str, validation: Dict[str, Any]):
        try:
            file_size = Path(filepath).stat().st_size
            
            if file_size < 1024: 
                validation['warnings'].append('PDF file is very small (may be corrupted)')
            with open(filepath, 'rb') as f:
                content = f.read()
                if b'%%EOF' not in content[-1000:]:
                    validation['warnings'].append('PDF may be missing EOF marker')
                            