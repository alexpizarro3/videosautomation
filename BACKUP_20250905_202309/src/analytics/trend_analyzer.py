import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import Counter
import re

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import load_json_file, save_json_file, get_trending_hashtags

class TrendAnalyzer:
    """Analizador de tendencias para videos de TikTok"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def analyze_video_performance(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizar rendimiento de videos"""
        self.logger.info(f"Analizando rendimiento de {len(videos)} videos")
        
        if not videos:
            return {}
        
        # Convertir a DataFrame para análisis
        df = pd.DataFrame(videos)
        
        # Análisis de métricas básicas
        metrics_analysis = {
            'total_videos': len(videos),
            'avg_likes': df['likes'].mean() if 'likes' in df else 0,
            'avg_comments': df['comments'].mean() if 'comments' in df else 0,
            'avg_shares': df['shares'].mean() if 'shares' in df else 0,
            'avg_views': df['views'].mean() if 'views' in df else 0,
            'avg_engagement_rate': df['engagement_rate'].mean() if 'engagement_rate' in df else 0,
        }
        
        # Videos de mejor rendimiento
        if 'engagement_rate' in df:
            top_performers = df.nlargest(5, 'engagement_rate')[
                ['title', 'likes', 'comments', 'shares', 'engagement_rate', 'hashtags']
            ].to_dict('records')
        else:
            top_performers = []
        
        # Análisis de hashtags más exitosos
        hashtag_analysis = self._analyze_hashtags(videos)
        
        # Análisis de patrones de contenido
        content_patterns = self._analyze_content_patterns(videos)
        
        # Tendencias temporales
        temporal_trends = self._analyze_temporal_trends(videos)
        
        analysis = {
            'analysis_date': datetime.now().isoformat(),
            'metrics_summary': metrics_analysis,
            'top_performers': top_performers,
            'hashtag_analysis': hashtag_analysis,
            'content_patterns': content_patterns,
            'temporal_trends': temporal_trends,
            'recommendations': self._generate_recommendations(
                metrics_analysis, hashtag_analysis, content_patterns
            )
        }
        
        self.logger.success("Análisis de rendimiento completado")
        return analysis
    
    def _analyze_hashtags(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizar rendimiento de hashtags"""
        hashtag_performance = {}
        hashtag_counts = Counter()
        
        for video in videos:
            hashtags = video.get('hashtags', [])
            engagement = video.get('engagement_rate', 0)
            likes = video.get('likes', 0)
            
            for hashtag in hashtags:
                hashtag = hashtag.lower()
                hashtag_counts[hashtag] += 1
                
                if hashtag not in hashtag_performance:
                    hashtag_performance[hashtag] = {
                        'count': 0,
                        'total_engagement': 0,
                        'total_likes': 0,
                        'videos': []
                    }
                
                hashtag_performance[hashtag]['count'] += 1
                hashtag_performance[hashtag]['total_engagement'] += engagement
                hashtag_performance[hashtag]['total_likes'] += likes
                hashtag_performance[hashtag]['videos'].append(video.get('title', ''))
        
        # Calcular promedio de rendimiento por hashtag
        for hashtag in hashtag_performance:
            count = hashtag_performance[hashtag]['count']
            hashtag_performance[hashtag]['avg_engagement'] = (
                hashtag_performance[hashtag]['total_engagement'] / count
            )
            hashtag_performance[hashtag]['avg_likes'] = (
                hashtag_performance[hashtag]['total_likes'] / count
            )
        
        # Top hashtags por engagement
        top_hashtags_engagement = sorted(
            hashtag_performance.items(),
            key=lambda x: x[1]['avg_engagement'],
            reverse=True
        )[:10]
        
        # Top hashtags por frecuencia
        top_hashtags_frequency = hashtag_counts.most_common(10)
        
        return {
            'total_unique_hashtags': len(hashtag_performance),
            'top_by_engagement': [
                {
                    'hashtag': hashtag,
                    'avg_engagement': data['avg_engagement'],
                    'avg_likes': data['avg_likes'],
                    'frequency': data['count']
                }
                for hashtag, data in top_hashtags_engagement
            ],
            'top_by_frequency': [
                {'hashtag': hashtag, 'count': count}
                for hashtag, count in top_hashtags_frequency
            ],
            'trending_suggestions': get_trending_hashtags()
        }
    
    def _analyze_content_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizar patrones en el contenido"""
        # Análisis de palabras clave en títulos
        all_titles = [video.get('title', '') for video in videos]
        word_frequency = self._analyze_word_frequency(all_titles)
        
        # Análisis de longitud de títulos
        title_lengths = [len(title) for title in all_titles if title]
        avg_title_length = np.mean(title_lengths) if title_lengths else 0
        
        # Análisis de emojis
        emoji_usage = self._analyze_emoji_usage(all_titles)
        
        # Patrones de engagement por tipo de contenido
        content_types = self._categorize_content(videos)
        
        return {
            'word_frequency': word_frequency,
            'avg_title_length': avg_title_length,
            'emoji_usage': emoji_usage,
            'content_types': content_types,
            'title_patterns': self._identify_title_patterns(all_titles)
        }
    
    def _analyze_word_frequency(self, titles: List[str]) -> List[Dict[str, Any]]:
        """Analizar frecuencia de palabras en títulos"""
        # Combinar todos los títulos
        all_text = ' '.join(titles).lower()
        
        # Limpiar y dividir en palabras
        words = re.findall(r'\b\w+\b', all_text)
        
        # Filtrar palabras comunes (stop words básicas en español)
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo',
            'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las',
            'me', 'mi', 'tu', 'si', 'yo', 'he', 'ha', 'ya', 'muy', 'mas', 'como'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Contar frecuencia
        word_counts = Counter(filtered_words)
        
        return [
            {'word': word, 'count': count}
            for word, count in word_counts.most_common(20)
        ]
    
    def _analyze_emoji_usage(self, titles: List[str]) -> Dict[str, Any]:
        """Analizar uso de emojis"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticonos
            "\U0001F300-\U0001F5FF"  # símbolos & pictogramas
            "\U0001F680-\U0001F6FF"  # transporte & símbolos del mapa
            "\U0001F1E0-\U0001F1FF"  # banderas (iOS)
            "]+",
            flags=re.UNICODE
        )
        
        all_emojis = []
        videos_with_emojis = 0
        
        for title in titles:
            emojis = emoji_pattern.findall(title)
            if emojis:
                videos_with_emojis += 1
                all_emojis.extend(emojis)
        
        emoji_counts = Counter(all_emojis)
        
        return {
            'videos_with_emojis': videos_with_emojis,
            'emoji_usage_rate': videos_with_emojis / len(titles) if titles else 0,
            'most_used_emojis': [
                {'emoji': emoji, 'count': count}
                for emoji, count in emoji_counts.most_common(10)
            ]
        }
    
    def _categorize_content(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorizar contenido por tipo"""
        categories = {
            'educational': ['tutorial', 'how to', 'learn', 'tip', 'hack', 'guide'],
            'entertainment': ['funny', 'meme', 'lol', 'comedy', 'humor'],
            'lifestyle': ['daily', 'routine', 'life', 'day in', 'vlog'],
            'dance': ['dance', 'dancing', 'choreography', 'moves'],
            'food': ['food', 'recipe', 'cooking', 'eat', 'delicious'],
            'fashion': ['outfit', 'style', 'fashion', 'clothes', 'look'],
            'tech': ['tech', 'technology', 'app', 'phone', 'gadget']
        }
        
        content_stats = {category: {'count': 0, 'total_engagement': 0} for category in categories}
        uncategorized = 0
        
        for video in videos:
            title = video.get('title', '').lower()
            engagement = video.get('engagement_rate', 0)
            categorized = False
            
            for category, keywords in categories.items():
                if any(keyword in title for keyword in keywords):
                    content_stats[category]['count'] += 1
                    content_stats[category]['total_engagement'] += engagement
                    categorized = True
                    break
            
            if not categorized:
                uncategorized += 1
        
        # Calcular engagement promedio por categoría
        for category in content_stats:
            if content_stats[category]['count'] > 0:
                content_stats[category]['avg_engagement'] = (
                    content_stats[category]['total_engagement'] / content_stats[category]['count']
                )
            else:
                content_stats[category]['avg_engagement'] = 0
        
        return {
            'categories': content_stats,
            'uncategorized': uncategorized,
            'most_successful_category': max(
                content_stats.items(),
                key=lambda x: x[1]['avg_engagement']
            )[0] if any(stats['count'] > 0 for stats in content_stats.values()) else None
        }
    
    def _identify_title_patterns(self, titles: List[str]) -> List[str]:
        """Identificar patrones comunes en títulos"""
        patterns = []
        
        # Patrones de preguntas
        question_count = sum(1 for title in titles if '?' in title)
        if question_count > len(titles) * 0.2:  # Más del 20%
            patterns.append("Frequent use of questions")
        
        # Patrones de números
        number_count = sum(1 for title in titles if any(char.isdigit() for char in title))
        if number_count > len(titles) * 0.3:  # Más del 30%
            patterns.append("Frequent use of numbers")
        
        # Patrones de exclamación
        exclamation_count = sum(1 for title in titles if '!' in title)
        if exclamation_count > len(titles) * 0.4:  # Más del 40%
            patterns.append("High use of exclamation marks")
        
        # Patrones de mayúsculas
        caps_count = sum(1 for title in titles if title.isupper())
        if caps_count > len(titles) * 0.1:  # Más del 10%
            patterns.append("Frequent use of all caps")
        
        return patterns
    
    def _analyze_temporal_trends(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizar tendencias temporales"""
        # Para una implementación completa, necesitaríamos fechas de publicación
        # Por ahora, analizamos basado en fecha de scraping
        
        return {
            'analysis_note': 'Temporal analysis requires publication dates',
            'scraped_date': datetime.now().isoformat(),
            'video_count': len(videos)
        }
    
    def _generate_recommendations(self, metrics: Dict, hashtags: Dict, content: Dict) -> List[str]:
        """Generar recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones de hashtags
        if hashtags.get('top_by_engagement'):
            top_hashtag = hashtags['top_by_engagement'][0]['hashtag']
            recommendations.append(f"Use the hashtag '{top_hashtag}' which shows highest engagement")
        
        # Recomendaciones de tipo de contenido
        if content.get('content_types', {}).get('most_successful_category'):
            best_category = content['content_types']['most_successful_category']
            recommendations.append(f"Focus on {best_category} content for better engagement")
        
        # Recomendaciones de longitud de título
        avg_length = content.get('avg_title_length', 0)
        if avg_length > 0:
            if avg_length < 30:
                recommendations.append("Consider longer, more descriptive titles")
            elif avg_length > 100:
                recommendations.append("Consider shorter, punchier titles")
        
        # Recomendaciones de emojis
        emoji_rate = content.get('emoji_usage', {}).get('emoji_usage_rate', 0)
        if emoji_rate < 0.3:
            recommendations.append("Add more emojis to titles for better engagement")
        
        # Recomendaciones generales
        if metrics.get('avg_engagement_rate', 0) < 2:
            recommendations.append("Focus on creating more engaging content to improve interaction rates")
        
        return recommendations
    
    def save_analysis(self, analysis: Dict[str, Any], username: str) -> str:
        """Guardar análisis en archivo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analysis_{username}_{timestamp}.json"
        filepath = config.get_data_dir('metrics')
        filepath = f"{filepath}/{filename}"
        
        if save_json_file(analysis, filepath):
            self.logger.success(f"Análisis guardado en: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando análisis")
            return ""

# Función auxiliar para uso directo
def analyze_tiktok_trends(videos: List[Dict[str, Any]], username: str = "user") -> Dict[str, Any]:
    """Función auxiliar para analizar tendencias"""
    analyzer = TrendAnalyzer()
    analysis = analyzer.analyze_video_performance(videos)
    
    if analysis:
        analyzer.save_analysis(analysis, username)
    
    return analysis
