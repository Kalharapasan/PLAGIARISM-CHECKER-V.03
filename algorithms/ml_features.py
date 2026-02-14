import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, Union
from collections import Counter, defaultdict
import pickle
import json
import warnings
from pathlib import Path
import hashlib
from datetime import datetime

warnings.filterwarnings('ignore')

class MLFeatures:
    
    
    def _initialize_ml_components(self):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
            from sklearn.preprocessing import StandardScaler, MinMaxScaler
            from sklearn.decomposition import PCA, TruncatedSVD, LatentDirichletAllocation
            from sklearn.cluster import KMeans, DBSCAN
            from sklearn.ensemble import IsolationForest
            from sklearn.neighbors import LocalOutlierFactor
            self.vectorizers['tfidf'] = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=2,
                max_df=0.95
            )
            
            self.vectorizers['count'] = CountVectorizer(
                max_features=3000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            self.vectorizers['char'] = CountVectorizer(
                analyzer='char',
                ngram_range=(3, 5),
                max_features=2000
            )
            self.models['scaler'] = StandardScaler()
            self.models['minmax'] = MinMaxScaler()
            self.models['pca'] = PCA(n_components=50, random_state=42)
            self.models['svd'] = TruncatedSVD(n_components=100, random_state=42)
            self.models['lda'] = LatentDirichletAllocation(
                n_components=10,
                random_state=42,
                max_iter=10
            )
            self.models['kmeans'] = KMeans(n_clusters=5, random_state=42)
            self.models['dbscan'] = DBSCAN(eps=0.5, min_samples=5)
            self.models['isolation_forest'] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            self.models['lof'] = LocalOutlierFactor(
                contamination=0.1,
                novelty=True
            )
            
            print("✓ ML components initialized successfully")
        
        except ImportError as e:
            print(f"⚠ Some ML components not available: {e}")
    
    def extract_linguistic_features(self, text: str) -> Dict[str, float]:
        features['char_count'] = len(text)
        features['word_count'] = len(text.split())
        features['sentence_count'] = self._count_sentences(text)
        features['paragraph_count'] = self._count_paragraphs(text)
        words = text.split()
        if words:
            features['avg_word_length'] = sum(len(w) for w in words) / len(words)
            features['max_word_length'] = max(len(w) for w in words)
            features['unique_word_ratio'] = len(set(words)) / len(words)
            word_freq = Counter(words)
            features['vocabulary_richness'] = len(word_freq) / len(words)
            common_words = {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 'it'}
            common_word_count = sum(1 for w in words if w.lower() in common_words)
            features['common_word_ratio'] = common_word_count / len(words)
        if text:
            features['digit_ratio'] = sum(c.isdigit() for c in text) / len(text)
            features['letter_ratio'] = sum(c.isalpha() for c in text) / len(text)
            features['space_ratio'] = sum(c.isspace() for c in text) / len(text)
            features['punctuation_ratio'] = sum(c in '.,;:!?\'"()-[]{}' for c in text) / len(text)
            features['uppercase_ratio'] = sum(c.isupper() for c in text) / len(text)
        features['avg_sentence_length'] = features['word_count'] / max(features['sentence_count'], 1)
        features['avg_paragraph_length'] = features['sentence_count'] / max(features['paragraph_count'], 1)
        complex_words = [w for w in words if len(w) > 6]
        features['complex_word_ratio'] = len(complex_words) / max(len(words), 1)
        hapax_count = sum(1 for word, count in word_freq.items() if count == 1)
        features['hapax_legomena_ratio'] = hapax_count / max(len(word_freq), 1)
        
        return features
    
    def extract_stylometric_features(self, text: str) -> Dict[str, float]:
        features = {}
        function_words = {
            'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'was', 'he', 'for', 'it',
            'with', 'as', 'his', 'on', 'be', 'at', 'by', 'I', 'this', 'had', 'not', 'are',
            'but', 'from', 'or', 'have', 'an', 'they', 'which', 'one', 'you', 'were', 'her',
            'all', 'she', 'there', 'would', 'their', 'we', 'him', 'been', 'has', 'when',
            'who', 'will', 'more', 'no', 'if', 'out', 'so', 'said', 'what', 'up', 'its',
            'about', 'into', 'than', 'them', 'can', 'only', 'other', 'new', 'some', 'could',
            'time', 'these', 'two', 'may', 'then', 'do', 'first', 'any', 'my', 'now', 'such',
            'like', 'our', 'over', 'man', 'me', 'even', 'most', 'made', 'after', 'also',
            'did', 'many', 'before', 'must', 'through', 'back', 'years', 'where', 'much',
            'your', 'way', 'well', 'should', 'because', 'each', 'just', 'those', 'people',
            'how', 'too', 'little', 'state', 'good', 'very', 'make', 'world', 'still',
            'own', 'see', 'men', 'work', 'long', 'get', 'here', 'between', 'both', 'life',
            'being', 'under', 'never', 'day', 'same', 'another', 'know', 'while', 'last',
            'might', 'us', 'great', 'old', 'year', 'off', 'come', 'since', 'against',
            'go', 'came', 'right', 'used', 'take', 'three'
        }
        
        words = text.lower().split()
        if words:
            function_word_count = sum(1 for w in words if w in function_words)
            features['function_word_ratio'] = function_word_count / len(words)
        pos_tags = self._estimate_pos_tags(text)
        for pos, count in pos_tags.items():
            features[f'pos_{pos}_ratio'] = count / max(sum(pos_tags.values()), 1)
        sentences = self._extract_sentences(text)
        if sentences:
            sent_lengths = [len(s.split()) for s in sentences]
            features['sentence_length_mean'] = np.mean(sent_lengths)
            features['sentence_length_std'] = np.std(sent_lengths)
            features['sentence_length_cv'] = features['sentence_length_std'] / max(features['sentence_length_mean'], 1)
            sentence_beginnings = [s.split()[0].lower() if s.split() else '' for s in sentences[:50]]
            conjunction_beginnings = sum(1 for w in sentence_beginnings if w in {'and', 'but', 'or', 'however', 'therefore', 'thus', 'hence'})
            features['conjunction_sentence_start_ratio'] = conjunction_beginnings / len(sentences)
        sophisticated_words = self._identify_sophisticated_words(text)
        features['sophisticated_word_ratio'] = len(sophisticated_words) / max(len(words), 1)
        punctuation_counts = Counter(c for c in text if c in '.,;:!?\'"()-[]{}')
        for punct, count in punctuation_counts.items():
            features[f'punctuation_{punct}_ratio'] = count / max(len(text), 1)
        word_lengths = [len(w) for w in words]
        if word_lengths:
            features['word_length_mean'] = np.mean(word_lengths)
            features['word_length_std'] = np.std(word_lengths)
            features['word_length_skew'] = self._calculate_skewness(word_lengths)
        ttr_segments = self._calculate_ttr_segments(text)
        features['ttr_mean'] = np.mean(ttr_segments)
        features['ttr_std'] = np.std(ttr_segments)
        word_freq = Counter(words)
        dislegomena_count = sum(1 for count in word_freq.values() if count == 2)
        features['dislegomena_ratio'] = dislegomena_count / max(len(word_freq), 1)
        
        return features
    
    def extract_nlp_features(self, text: str) -> Dict[str, Any]:
        features = {}
        spacy_features = self._extract_spacy_features(text)
        features.update(spacy_features)
        nltk_features = self._extract_nltk_features(text)
        features.update(nltk_features)
        graph_features = self._extract_graph_features(text)
        features.update(graph_features)
        semantic_features = self._extract_semantic_features(text)
        features.update(semantic_features)        
        return features
    
    def extract_embedding_features(self, text: str, 
                                 method: str = 'tfidf') -> np.ndarray:
        if method not in self.vectorizers and method not in self.models:
            raise ValueError(f"Unsupported embedding method: {method}")
        cache_key = f"{hashlib.md5(text.encode()).hexdigest()}_{method}"
        if cache_key in self.feature_cache:
            return self.feature_cache[cache_key]
        
        try:
            if method == 'tfidf':
                vectorizer = self.vectorizers['tfidf']
                embedding = vectorizer.fit_transform([text]).toarray()[0]
            
            elif method == 'count':
                vectorizer = self.vectorizers['count']
                embedding = vectorizer.fit_transform([text]).toarray()[0]
            
            elif method == 'char':
                vectorizer = self.vectorizers['char']
                embedding = vectorizer.fit_transform([text]).toarray()[0]
            
            elif method == 'svd':
                tfidf_vec = self.vectorizers['tfidf']
                tfidf_matrix = tfidf_vec.fit_transform([text])
                svd_model = self.models['svd']
                embedding = svd_model.fit_transform(tfidf_matrix).flatten()
            
            elif method == 'lda':
                count_vec = self.vectorizers['count']
                count_matrix = count_vec.fit_transform([text])
                lda_model = self.models['lda']
                embedding = lda_model.fit_transform(count_matrix).flatten()
            
            else:
                vectorizer = self.vectorizers['tfidf']
                embedding = vectorizer.fit_transform([text]).toarray()[0]
            self.feature_cache[cache_key] = embedding
            
            return embedding
        except Exception as e:
            print(f"Warning: Embedding extraction failed: {e}")
            if method in ['tfidf', 'count']:
                return np.zeros(5000)
            elif method == 'char':
                return np.zeros(2000)
            elif method == 'svd':
                return np.zeros(100)
            elif method == 'lda':
                return np.zeros(10)
            else:
                return np.zeros(100)
    
    def extract_all_features(self, text: str) -> Dict[str, Any]:
        all_features = {}
        linguistic = self.extract_linguistic_features(text)
        all_features['linguistic'] = linguistic
        stylometric = self.extract_stylometric_features(text)
        all_features['stylometric'] = stylometric
        nlp = self.extract_nlp_features(text)
        all_features['nlp'] = nlp
        embeddings = {}
        for method in ['tfidf', 'count', 'char', 'svd', 'lda']:
            try:
                embedding = self.extract_embedding_features(text, method)
                embeddings[method] = embedding.tolist()
            except:
                pass
        
        all_features['embeddings'] = embeddings
        combined_vector = self._create_combined_feature_vector(text)
        all_features['combined_vector'] = combined_vector.tolist()
        all_features['metadata'] = {
            'text_length': len(text),
            'feature_extraction_time': datetime.now().isoformat(),
            'total_features': len(combined_vector)
        }
        
        return all_features
    
    def detect_plagiarism_patterns(self, text: str, 
                                 reference_texts: List[str] = None) -> Dict[str, Any]:
        results = {
            'plagiarism_score': 0.0,
            'pattern_matches': [],
            'anomaly_scores': {},
            'cluster_assignment': None,
            'recommendations': []
        }
        features = self.extract_all_features(text)
        anomaly_scores = self._calculate_anomaly_scores(features['combined_vector'])
        results['anomaly_scores'] = anomaly_scores
        if reference_texts:
            similarities = []
            for ref_text in reference_texts:
                sim_score = self._calculate_feature_similarity(text, ref_text)
                similarities.append(sim_score)
            
            if similarities:
                results['reference_similarities'] = {
                    'mean': np.mean(similarities),
                    'max': np.max(similarities),
                    'min': np.min(similarities),
                    'std': np.std(similarities)
                }
                results['plagiarism_score'] = np.max(similarities)
        
        patterns = self._detect_specific_patterns(text, features)
        results['pattern_matches'] = patterns
        
        try:
            if 'combined_vector' in features:
                cluster_id = self._assign_to_cluster(features['combined_vector'])
                results['cluster_assignment'] = cluster_id
        except:
            pass
        
        recommendations = self._generate_recommendations(results)
        results['recommendations'] = recommendations
        
        return results
    
    def train_plagiarism_classifier(self, texts: List[str], 
                                  labels: List[int],
                                  model_type: str = 'ensemble') -> Dict[str, Any]:
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import classification_report, confusion_matrix
            from sklearn.linear_model import LogisticRegression
            from sklearn.svm import SVC
            from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
            from sklearn.naive_bayes import MultinomialNB
            import xgboost as xgb
            
            print("Extracting features...")
            feature_vectors = []
            for text in texts:
                features = self.extract_all_features(text)
                vector = features['combined_vector']
                feature_vectors.append(vector)
            
            X = np.array(feature_vectors)
            y = np.array(labels)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            print(f"Training {model_type} classifier...")
            
            if model_type == 'logistic':
                model = LogisticRegression(random_state=42, max_iter=1000)
            elif model_type == 'svm':
                model = SVC(random_state=42, probability=True)
            elif model_type == 'random_forest':
                model = RandomForestClassifier(random_state=42, n_estimators=100)
            elif model_type == 'gradient_boosting':
                model = GradientBoostingClassifier(random_state=42)
            elif model_type == 'naive_bayes':
                model = MultinomialNB()
            elif model_type == 'xgboost':
                model = xgb.XGBClassifier(random_state=42)
            elif model_type == 'ensemble':
                from sklearn.ensemble import VotingClassifier
                models = [
                    ('lr', LogisticRegression(random_state=42, max_iter=1000)),
                    ('rf', RandomForestClassifier(random_state=42, n_estimators=50)),
                    ('svm', SVC(random_state=42, probability=True))
                ]
                model = VotingClassifier(estimators=models, voting='soft')
            else:
                model = RandomForestClassifier(random_state=42)
            
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
            
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1_score': f1_score(y_test, y_pred, zero_division=0),
                'roc_auc': roc_auc_score(y_test, y_pred_proba)
            }
            
            cm = confusion_matrix(y_test, y_pred)
            cm_dict = {
                'true_negative': int(cm[0, 0]),
                'false_positive': int(cm[0, 1]),
                'false_negative': int(cm[1, 0]),
                'true_positive': int(cm[1, 1])
            }
            self.models['plagiarism_classifier'] = model
            
            return {
                'model_type': model_type,
                'metrics': metrics,
                'confusion_matrix': cm_dict,
                'feature_importance': self._get_feature_importance(model, X.shape[1]),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
        
        except ImportError as e:
            return {'error': f"Required libraries not available: {e}"}
        except Exception as e:
            return {'error': f"Training failed: {e}"}
    
    def predict_plagiarism(self, text: str) -> Dict[str, Any]:
        if 'plagiarism_classifier' not in self.models:
            return {'error': 'No trained classifier available'}
        
        try:
            features = self.extract_all_features(text)
            X = features['combined_vector'].reshape(1, -1)
            model = self.models['plagiarism_classifier']
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0][1]
            contributions = self._get_feature_contributions(model, X[0])
            
            return {
                'is_plagiarized': bool(prediction),
                'plagiarism_probability': float(probability),
                'confidence': self._calculate_confidence(probability),
                'feature_contributions': contributions[:10],  
                'recommendation': self._get_prediction_recommendation(probability)
            }
            
        except Exception as e:
            return {'error': f"Prediction failed: {e}"}
        
    def _count_sentences(self, text: str) -> int:
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        return len([s for s in sentences if len(s.strip()) > 5])

    def _count_paragraphs(self, text: str) -> int:
        paragraphs = text.split('\n\n')
        return len([p for p in paragraphs if len(p.strip()) > 20])
    
    def _estimate_pos_tags(self, text: str) -> Dict[str, int]:
        words = text.split()
        pos_counts = {
            'noun': 0,
            'verb': 0,
            'adjective': 0,
            'adverb': 0,
            'preposition': 0,
            'conjunction': 0,
            'pronoun': 0,
            'determiner': 0
        }
        nouns = {'time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life', 'hand'}
        verbs = {'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see'}
        adjectives = {'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 'old'}
        adverbs = {'not', 'also', 'very', 'often', 'well', 'too', 'just', 'more', 'so', 'now'}
        prepositions = {'of', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'about'}
        conjunctions = {'and', 'but', 'or', 'so', 'yet', 'for', 'nor', 'although', 'because'}
        pronouns = {'I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her'}
        determiners = {'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his'}
        
        for word in words:
            word_lower = word.lower()
            if word_lower in nouns:
                pos_counts['noun'] += 1
            elif word_lower in verbs:
                pos_counts['verb'] += 1
            elif word_lower in adjectives:
                pos_counts['adjective'] += 1
            elif word_lower in adverbs:
                pos_counts['adverb'] += 1
            elif word_lower in prepositions:
                pos_counts['preposition'] += 1
            elif word_lower in conjunctions:
                pos_counts['conjunction'] += 1
            elif word_lower in pronouns:
                pos_counts['pronoun'] += 1
            elif word_lower in determiners:
                pos_counts['determiner'] += 1
        
        return pos_counts
    
    def _extract_sentences(self, text: str) -> List[str]:
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _identify_sophisticated_words(self, text: str) -> List[str]:
        common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
            'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
            'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
            'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
            'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
            'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
            'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
            'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us'
        }
        words = text.lower().split()
        sophisticated = [w for w in words if len(w) > 6 and w not in common_words]
        common_suffixes = {'ing', 'ed', 'ly', 'tion', 'ment', 'ness', 'able', 'ible'}
        sophisticated = [w for w in sophisticated if not any(w.endswith(suffix) for suffix in common_suffixes)]
        return list(set(sophisticated))[:20]
    
    def _calculate_skewness(self, data: List[float]) -> float:
        if len(data) < 2:
            return 0.0
        
        data_array = np.array(data)
        mean = np.mean(data_array)
        std = np.std(data_array)
        
        if std == 0:
            return 0.0
        
        skewness = np.mean(((data_array - mean) / std) ** 3)
        return float(skewness)
    
    def _calculate_ttr_segments(self, text: str, segment_size: int = 100) -> List[float]:
        words = text.split()
        ttr_values = []
        
        for i in range(0, len(words), segment_size):
            segment = words[i:i + segment_size]
            if segment:
                unique_words = len(set(segment))
                ttr = unique_words / len(segment)
                ttr_values.append(ttr)
        
        return ttr_values
    
    def _extract_spacy_features(self, text: str) -> Dict[str, float]:
        features = {}
        try:
            import spacy
            if 'spacy_nlp' not in self.models:
                try:
                    self.models['spacy_nlp'] = spacy.load('en_core_web_sm')
                except:
                    import subprocess
                    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
                    self.models['spacy_nlp'] = spacy.load('en_core_web_sm')
            
            nlp = self.models['spacy_nlp']
            doc = nlp(text)
            features['spacy_token_count'] = len(doc)
            features['spacy_sentence_count'] = len(list(doc.sents))
            pos_counts = Counter([token.pos_ for token in doc])
            for pos, count in pos_counts.items():
                features[f'spacy_{pos.lower()}_ratio'] = count / len(doc)

            max_depth = 0
            for token in doc:
                depth = 0
                current = token
                while current.head != current:
                    depth += 1
                    current = current.head
                max_depth = max(max_depth, depth)
            
            features['spacy_max_dependency_depth'] = max_depth
            features['spacy_named_entity_count'] = len(doc.ents)
            unique_lemmas = len(set([token.lemma_ for token in doc]))
            features['spacy_unique_lemma_ratio'] = unique_lemmas / len(doc)
            
        except ImportError:
            pass
        except Exception as e:
            print(f"Warning: spaCy feature extraction failed: {e}")
        
        return features
    
    def _extract_nltk_features(self, text: str) -> Dict[str, float]:
        features = {}
        
        try:
            import nltk
            from nltk.tokenize import word_tokenize, sent_tokenize
            from nltk.corpus import stopwords
            from nltk import pos_tag
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                nltk.download('averaged_perceptron_tagger')
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
            
            words = word_tokenize(text.lower())
            sentences = sent_tokenize(text)
            pos_tags = pos_tag(words)
            pos_counts = Counter([tag for word, tag in pos_tags])
            pos_categories = {
                'NN': 'noun', 'NNS': 'noun', 'NNP': 'noun', 'NNPS': 'noun',
                'VB': 'verb', 'VBD': 'verb', 'VBG': 'verb', 'VBN': 'verb', 
                'VBP': 'verb', 'VBZ': 'verb',
                'JJ': 'adjective', 'JJR': 'adjective', 'JJS': 'adjective',
                'RB': 'adverb', 'RBR': 'adverb', 'RBS': 'adverb'
            }
            
            category_counts = defaultdict(int)
            for tag, count in pos_counts.items():
                category = pos_categories.get(tag, 'other')
                category_counts[category] += count
            
            for category, count in category_counts.items():
                features[f'nltk_{category}_ratio'] = count / len(words)
            stop_words = set(stopwords.words('english'))
            stopword_count = sum(1 for w in words if w in stop_words)
            features['nltk_stopword_ratio'] = stopword_count / len(words)
        
        except ImportError:
            pass
        except Exception as e:
            print(f"Warning: NLTK feature extraction failed: {e}")
        
        return features
    
    def _extract_graph_features(self, text: str) -> Dict[str, float]:
        features = {}
        try:
            words = text.lower().split()
            
            if len(words) < 10:
                return features
            cooccurrence = defaultdict(int)
            window_size = 3
            
            for i in range(len(words)):
                for j in range(i + 1, min(i + window_size, len(words))):
                    pair = tuple(sorted([words[i], words[j]]))
                    cooccurrence[pair] += 1
            
            features['graph_cooccurrence_pairs'] = len(cooccurrence)
            features['graph_avg_cooccurrence'] = np.mean(list(cooccurrence.values())) if cooccurrence else 0
        
        except Exception as e:
            print(f"Warning: Graph feature extraction failed: {e}")
        
        return features
    
    def _extract_semantic_features(self, text: str) -> Dict[str, float]:
        features = {}
        try:
            words = text.lower().split()
            academic_words = {
                'analysis', 'approach', 'area', 'assessment', 'assume', 'authority', 'available',
                'benefit', 'concept', 'consistent', 'constitutional', 'context', 'contract', 'create',
                'data', 'definition', 'derived', 'distribution', 'economic', 'environment', 'established',
                'estimate', 'evidence', 'export', 'factors', 'financial', 'formula', 'function',
                'identified', 'income', 'indicate', 'individual', 'interpretation', 'involved', 'issues',
                'labour', 'legal', 'legislation', 'major', 'method', 'occur', 'percent', 'period',
                'policy', 'principle', 'procedure', 'process', 'required', 'research', 'response',
                'role', 'section', 'sector', 'significant', 'similar', 'source', 'specific', 'structure',
                'theory', 'variables'
            }
            
            academic_count = sum(1 for w in words if w in academic_words)
            features['semantic_academic_word_ratio'] = academic_count / len(words)
            long_words = [w for w in words if len(w) > 8]
            features['semantic_long_word_ratio'] = len(long_words) / len(words)
        
        except Exception as e:
            print(f"Warning: Semantic feature extraction failed: {e}")
        
        return features
    
    def _create_combined_feature_vector(self, text: str) -> np.ndarray: