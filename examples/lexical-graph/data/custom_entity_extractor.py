import spacy
from typing import List, Dict, Any, Optional
from transformers import pipeline

class CustomEntityExtractor:
    """
    Custom entity extractor that combines multiple extraction methods:
    1. spaCy for basic named entity recognition
    2. Hugging Face transformers for specialized entity extraction
    3. Custom rule-based patterns for domain-specific entities
    """
    
    def __init__(self, custom_patterns: Optional[Dict[str, List[str]]] = None):
        # Initialize spaCy
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize transformer pipeline for token classification
        self.ner_pipeline = pipeline(
            "token-classification",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
        
        # Custom patterns for rule-based matching
        self.custom_patterns = custom_patterns or {}
        if custom_patterns:
            self._add_custom_patterns()
    
    def _add_custom_patterns(self):
        """Add custom patterns to spaCy's rule-based matcher"""
        from spacy.matcher import Matcher
        self.matcher = Matcher(self.nlp.vocab)
        
        for entity_type, patterns in self.custom_patterns.items():
            pattern_list = [[{"LOWER": word.lower()}] for word in patterns]
            self.matcher.add(entity_type, pattern_list)
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities using multiple methods and combine results.
        
        Args:
            text: Input text to extract entities from
            
        Returns:
            Dictionary with entity types as keys and lists of entity information as values
        """
        # Process with spaCy
        doc = self.nlp(text)
        spacy_entities = {
            ent.label_: {
                'text': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'source': 'spacy'
            }
            for ent in doc.ents
        }
        
        # Process with transformer pipeline
        transformer_entities = self.ner_pipeline(text)
        for ent in transformer_entities:
            entity_type = ent['entity_group']
            if entity_type not in spacy_entities:
                spacy_entities[entity_type] = []
            spacy_entities[entity_type].append({
                'text': ent['word'],
                'start': ent['start'],
                'end': ent['end'],
                'score': ent['score'],
                'source': 'transformer'
            })
        
        # Add custom pattern matches if defined
        if hasattr(self, 'matcher'):
            matches = self.matcher(doc)
            for match_id, start, end in matches:
                entity_type = self.nlp.vocab.strings[match_id]
                if entity_type not in spacy_entities:
                    spacy_entities[entity_type] = []
                spacy_entities[entity_type].append({
                    'text': doc[start:end].text,
                    'start': doc[start].idx,
                    'end': doc[end-1].idx + len(doc[end-1]),
                    'source': 'custom_pattern'
                })
        
        return spacy_entities

# Example custom patterns for technical documentation
TECHNICAL_PATTERNS = {
    'DATABASE': ['Neptune', 'PostgreSQL', 'MySQL', 'MongoDB', 'DynamoDB', 'Redis'],
    'CLOUD_SERVICE': [
        'AWS', 'Amazon Web Services', 'S3', 'EC2', 'Lambda', 'CloudFormation',
        'IAM', 'VPC', 'ECS', 'EKS', 'RDS', 'Aurora'
    ],
    'PROGRAMMING_LANGUAGE': [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'Go', 'Rust',
        'Ruby', 'PHP', 'Swift'
    ],
    'FRAMEWORK': [
        'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Express',
        'TensorFlow', 'PyTorch', 'Scikit-learn'
    ],
    'PROTOCOL': [
        'HTTP', 'HTTPS', 'TCP', 'UDP', 'SSH', 'FTP', 'SMTP', 'REST', 'GraphQL',
        'WebSocket'
    ],
    'TOOL': [
        'Git', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible',
        'Maven', 'Gradle', 'npm', 'pip'
    ]
} 