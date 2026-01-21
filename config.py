import json
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = self._get_default_config()
        self.config = self.load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "application": {
                "name": "Plagiarism Checker Pro",
                "version": "3.0",
                "author": "Academic Integrity Suite",
                "default_mode": "basic"
            },
            
            "database": {
                "path": "data/database.sqlite",
                "backup_enabled": True,
                "backup_count": 10,
                "auto_cleanup_days": 30
            },
            
            "detection": {
                "basic": {
                    "algorithms": ["cosine"],
                    "threshold": 15.0,
                    "min_match_length": 5
                },
                "advanced": {
                    "algorithms": ["cosine", "jaccard", "ngram", "sequence"],
                    "threshold": 10.0,
                    "min_match_length": 4,
                    "enable_citation_detection": True
                },
                "ultimate": {
                    "algorithms": ["cosine_tfidf", "cosine_count", "jaccard", 
                                  "overlap", "dice", "ngram_3", "ngram_5", 
                                  "sequence", "semantic", "lsi"],
                    "threshold": 5.0,
                    "min_match_length": 3,
                    "enable_ml": True,
                    "enable_nlp": True,
                    "enable_citations": True,
                    "enable_readability": True
                }
            },
            
            "file_handling": {
                "supported_formats": [".txt", ".docx", ".pdf", ".rtf", ".html", 
                                     ".htm", ".md", ".tex", ".odt", ".epub"],
                "max_file_size_mb": 50,
                "encoding": "utf-8",
                "temp_directory": "temp/"
            },
            
            "ui": {
                "basic": {
                    "theme": "light",
                    "font_family": "Arial",
                    "font_size": 10,
                    "window_size": "1000x700"
                },
                "advanced": {
                    "theme": "light",
                    "font_family": "Segoe UI",
                    "font_size": 9,
                    "window_size": "1400x900",
                    "show_analytics": True
                },
                "ultimate": {
                    "theme": "system",
                    "font_family": "Inter",
                    "font_size": 10,
                    "window_size": "1600x1000",
                    "show_all_panels": True
                }
            },
            
            "reporting": {
                "basic": {
                    "formats": ["txt"],
                    "include_summary": True,
                    "include_matches": True
                },
                "advanced": {
                    "formats": ["txt", "html"],
                    "include_summary": True,
                    "include_matches": True,
                    "include_statistics": True,
                    "include_recommendations": True
                },
                "ultimate": {
                    "formats": ["txt", "html", "pdf", "json"],
                    "include_summary": True,
                    "include_matches": True,
                    "include_statistics": True,
                    "include_recommendations": True,
                    "include_visualizations": True,
                    "include_nlp_analysis": True,
                    "include_readability": True
                }
            },
            
            "performance": {
                "max_threads": 4,
                "cache_enabled": True,
                "cache_size_mb": 100,
                "batch_chunk_size": 10
            },
            
            "paths": {
                "database": "data/database.sqlite",
                "reports": "reports/",
                "templates": "data/templates/",
                "logs": "logs/",
                "exports": "exports/"
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    return self._merge_configs(self.default_config, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config
        else:
            self.save_config(self.default_config)
            return self.default_config
    
    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        merged = default.copy()
        
        for key, value in custom.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def save_config(self, config: Dict = None):
        if config is None:
            config = self.config
        
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    def set(self, key: str, value: Any):
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()

config = Config()