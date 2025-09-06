#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SELECTOR INTELIGENTE DE IMÁGENES VIRALES
Evalúa y selecciona las mejores imágenes basándose en criterios de viralidad profesional
"""

import os
import glob
from PIL import Image
import json
from typing import List, Dict, Tuple
import colorsys
import numpy as np

class ViralImageSelector:
    """Selecciona las mejores imágenes para contenido viral"""
    
    def __init__(self):
        self.viral_criteria = {
            'color_vibrancy': 25,      # Colores vibrantes y llamativos
            'contrast_ratio': 20,      # Alto contraste visual
            'composition': 20,         # Composición equilibrada
            'visual_appeal': 15,       # Atractivo visual general
            'uniqueness': 10,          # Elementos únicos/distintivos
            'trend_potential': 10      # Potencial de tendencia
        }
    
    def analyze_image_vibrancy(self, image_path: str) -> Dict:
        """Analiza la vibración de colores de una imagen"""
        try:
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Redimensionar para análisis más rápido
                img = img.resize((100, 100))
                pixels = np.array(img)
                
                # Calcular métricas de color
                brightness = np.mean(pixels)
                saturation = self._calculate_saturation(pixels)
                contrast = self._calculate_contrast(pixels)
                color_variety = self._calculate_color_variety(pixels)
                
                return {
                    'brightness': brightness,
                    'saturation': saturation,
                    'contrast': contrast,
                    'color_variety': color_variety,
                    'file_size': os.path.getsize(image_path)
                }
        except Exception as e:
            print(f"❌ Error analizando {image_path}: {e}")
            return {
                'brightness': 50,
                'saturation': 50,
                'contrast': 50,
                'color_variety': 50,
                'file_size': 0
            }
    
    def _calculate_saturation(self, pixels: np.ndarray) -> float:
        """Calcula la saturación promedio de la imagen"""
        try:
            r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
            max_rgb = np.maximum(np.maximum(r, g), b)
            min_rgb = np.minimum(np.minimum(r, g), b)
            
            # Evitar división por cero
            saturation = np.where(max_rgb == 0, 0, (max_rgb - min_rgb) / max_rgb)
            return float(np.mean(saturation) * 100)
        except:
            return 50.0
    
    def _calculate_contrast(self, pixels: np.ndarray) -> float:
        """Calcula el contraste de la imagen"""
        try:
            gray = np.mean(pixels, axis=2)
            return float(np.std(gray))
        except:
            return 50.0
    
    def _calculate_color_variety(self, pixels: np.ndarray) -> float:
        """Calcula la variedad de colores únicos"""
        try:
            # Simplificar colores para contar variedad
            simplified = pixels // 32 * 32
            unique_colors = len(np.unique(simplified.reshape(-1, 3), axis=0))
            return min(unique_colors / 10.0, 100.0)  # Normalizar a 0-100
        except:
            return 50.0
    
    def score_viral_potential(self, image_path: str) -> Tuple[float, Dict]:
        """Calcula el score de potencial viral de una imagen"""
        metrics = self.analyze_image_vibrancy(image_path)
        
        # Criterios de scoring viral
        scores = {}
        
        # 1. Color Vibrancy (25 puntos)
        vibrancy_score = min(metrics['saturation'] / 100 * 25, 25)
        scores['color_vibrancy'] = vibrancy_score
        
        # 2. Contrast Ratio (20 puntos)
        contrast_score = min(metrics['contrast'] / 100 * 20, 20)
        scores['contrast_ratio'] = contrast_score
        
        # 3. Composition (20 puntos) - basado en brightness balance
        composition_score = 20 - abs(metrics['brightness'] - 128) / 128 * 20
        scores['composition'] = max(composition_score, 0)
        
        # 4. Visual Appeal (15 puntos) - combinación de factores
        appeal_score = (vibrancy_score + contrast_score) / 45 * 15
        scores['visual_appeal'] = appeal_score
        
        # 5. Uniqueness (10 puntos) - basado en variedad de colores
        uniqueness_score = min(metrics['color_variety'] / 100 * 10, 10)
        scores['uniqueness'] = uniqueness_score
        
        # 6. Trend Potential (10 puntos) - basado en características actuales
        trend_score = self._calculate_trend_potential(metrics)
        scores['trend_potential'] = trend_score
        
        total_score = sum(scores.values())
        
        analysis = {
            'total_score': round(total_score, 2),
            'scores_breakdown': scores,
            'metrics': metrics,
            'viral_rating': self._get_viral_rating(total_score)
        }
        
        return total_score, analysis
    
    def _calculate_trend_potential(self, metrics: Dict) -> float:
        """Calcula potencial de tendencia basado en características actuales"""
        score = 0
        
        # Tendencias 2025: Colores pasteles y vibrantes
        if 40 <= metrics['saturation'] <= 80:  # Saturación media-alta
            score += 4
        
        # Contraste medio-alto es viral
        if metrics['contrast'] > 30:
            score += 3
        
        # Brightness balanceada
        if 80 <= metrics['brightness'] <= 180:
            score += 3
        
        return min(score, 10)
    
    def _get_viral_rating(self, score: float) -> str:
        """Convierte score numérico a rating cualitativo"""
        if score >= 80:
            return "🔥 ULTRA VIRAL"
        elif score >= 70:
            return "🚀 ALTO POTENCIAL"
        elif score >= 60:
            return "⚡ BUEN POTENCIAL"
        elif score >= 50:
            return "📈 POTENCIAL MEDIO"
        else:
            return "📊 POTENCIAL BAJO"
    
    def select_best_images(self, images_dir: str = "data/images", num_select: int = 3) -> List[Dict]:
        """Selecciona las mejores imágenes para contenido viral"""
        print(f"\n🎯 SELECTOR INTELIGENTE DE IMÁGENES VIRALES")
        print("=" * 60)
        
        # Encontrar todas las imágenes gemini
        image_patterns = [
            f"{images_dir}/gemini_image_*.png",
            f"{images_dir}/gemini_image_*.jpg", 
            f"{images_dir}/gemini_image_*.jpeg"
        ]
        
        all_images = []
        for pattern in image_patterns:
            all_images.extend(glob.glob(pattern))
        
        if not all_images:
            print(f"❌ No se encontraron imágenes en {images_dir}")
            return []
        
        print(f"🔍 Analizando {len(all_images)} imágenes...")
        
        # Analizar cada imagen
        image_analyses = []
        for i, image_path in enumerate(all_images, 1):
            print(f"   📸 Analizando imagen {i}/{len(all_images)}: {os.path.basename(image_path)}")
            
            score, analysis = self.score_viral_potential(image_path)
            
            image_data = {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'score': score,
                'analysis': analysis
            }
            
            image_analyses.append(image_data)
            
            print(f"      🎯 Score: {score:.1f}/100 - {analysis['viral_rating']}")
        
        # Ordenar por score descendente
        image_analyses.sort(key=lambda x: x['score'], reverse=True)
        
        # Seleccionar las mejores
        best_images = image_analyses[:num_select]
        
        print(f"\n🏆 TOP {num_select} IMÁGENES SELECCIONADAS:")
        print("=" * 60)
        
        for i, img_data in enumerate(best_images, 1):
            analysis = img_data['analysis']
            print(f"\n🥇 POSICIÓN {i}: {img_data['filename']}")
            print(f"   🎯 Score Total: {img_data['score']:.1f}/100")
            print(f"   🔥 Rating: {analysis['viral_rating']}")
            print(f"   📊 Desglose:")
            print(f"      • Color Vibrancy: {analysis['scores_breakdown']['color_vibrancy']:.1f}/25")
            print(f"      • Contrast: {analysis['scores_breakdown']['contrast_ratio']:.1f}/20")
            print(f"      • Composition: {analysis['scores_breakdown']['composition']:.1f}/20")
            print(f"      • Visual Appeal: {analysis['scores_breakdown']['visual_appeal']:.1f}/15")
            print(f"      • Uniqueness: {analysis['scores_breakdown']['uniqueness']:.1f}/10")
            print(f"      • Trend Potential: {analysis['scores_breakdown']['trend_potential']:.1f}/10")
        
        # Guardar reporte
        self._save_selection_report(image_analyses, best_images)
        
        return best_images
    
    def _save_selection_report(self, all_analyses: List[Dict], selected: List[Dict]):
        """Guarda reporte detallado de la selección"""
        report = {
            'selection_date': '2025-09-03',
            'total_images_analyzed': len(all_analyses),
            'selected_count': len(selected),
            'selection_criteria': self.viral_criteria,
            'all_images': all_analyses,
            'selected_images': selected,
            'average_score': sum(img['score'] for img in all_analyses) / len(all_analyses) if all_analyses else 0
        }
        
        os.makedirs('data/analytics', exist_ok=True)
        report_path = 'data/analytics/viral_image_selection_report.json'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte guardado: {report_path}")

def main():
    """Función principal para testing"""
    selector = ViralImageSelector()
    best_images = selector.select_best_images()
    
    if best_images:
        print(f"\n✅ Selección completada: {len(best_images)} imágenes listas para viralización")
    else:
        print("\n❌ No se pudieron seleccionar imágenes")

if __name__ == "__main__":
    main()
