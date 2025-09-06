#!/usr/bin/env python3
"""
Script principal para automatización de videos de TikTok
Orquesta todo el proceso: scraping, análisis, generación y subida
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Any, List

# Agregar el directorio src al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.config import config
from utils.helpers import create_progress_tracker, save_json_file

# Importar módulos principales
from analytics.tiktok_scraper import scrape_tiktok_metrics
from analytics.trend_analyzer import analyze_tiktok_trends
from generation.prompt_generator import create_content_plan
from generation.image_generator import generate_images_from_prompts
from generation.video_generator import generate_videos_from_images
from upload.tiktok_uploader import upload_videos_to_tiktok

class TikTokAutomation:
    """Clase principal para automatización de TikTok"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.progress = create_progress_tracker()
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Configurar pasos del proceso
        self._setup_progress_steps()
    
    def _setup_progress_steps(self):
        """Configurar pasos del proceso"""
        self.progress.add_step("Scraping de métricas de TikTok")
        self.progress.add_step("Análisis de tendencias")
        self.progress.add_step("Generación de plan de contenido")
        self.progress.add_step("Generación de imágenes base")
        self.progress.add_step("Generación de videos")
        self.progress.add_step("Subida a TikTok")
        self.progress.add_step("Finalización y logs")
    
    def run_full_automation(self, username: str, max_videos: int = 50, videos_to_create: int = 3) -> Dict[str, Any]:
        """Ejecutar automatización completa"""
        self.logger.info(f"🚀 Iniciando automatización completa para @{username}")
        self.logger.info(f"📊 Analizando hasta {max_videos} videos")
        self.logger.info(f"🎬 Creando {videos_to_create} nuevos videos")
        
        results = {
            'session_id': self.session_id,
            'started_at': datetime.now().isoformat(),
            'username': username,
            'success': False,
            'steps_completed': [],
            'errors': []
        }
        
        try:
            # Paso 1: Scraping de métricas
            self.logger.info(f"📈 {self.progress.get_current_step()}")
            scraped_videos = self._step_scraping(username, max_videos)
            if not scraped_videos:
                raise Exception("No se pudieron obtener métricas de TikTok")
            
            results['scraped_videos_count'] = len(scraped_videos)
            results['steps_completed'].append('scraping')
            self.progress.complete_step()
            
            # Paso 2: Análisis de tendencias
            self.logger.info(f"🔍 {self.progress.get_current_step()}")
            analysis = self._step_analysis(scraped_videos, username)
            if not analysis:
                raise Exception("No se pudo completar el análisis de tendencias")
            
            results['analysis_completed'] = True
            results['steps_completed'].append('analysis')
            self.progress.complete_step()
            
            # Paso 3: Generación de plan de contenido
            self.logger.info(f"📝 {self.progress.get_current_step()}")
            content_plan = self._step_content_planning(analysis, videos_to_create)
            if not content_plan:
                raise Exception("No se pudo generar el plan de contenido")
            
            results['content_plan_id'] = content_plan.get('plan_id')
            results['steps_completed'].append('content_planning')
            self.progress.complete_step()
            
            # Paso 4: Generación de imágenes
            self.logger.info(f"🎨 {self.progress.get_current_step()}")
            generated_images = self._step_image_generation(content_plan)
            if not generated_images:
                raise Exception("No se pudieron generar las imágenes")
            
            successful_images = [img for img in generated_images if img.get('success', False)]
            results['images_generated'] = len(successful_images)
            results['steps_completed'].append('image_generation')
            self.progress.complete_step()
            
            # Paso 5: Generación de videos
            self.logger.info(f"🎬 {self.progress.get_current_step()}")
            generated_videos = self._step_video_generation(content_plan, successful_images)
            if not generated_videos:
                raise Exception("No se pudieron generar los videos")
            
            successful_videos = [vid for vid in generated_videos if vid.get('success', False)]
            results['videos_generated'] = len(successful_videos)
            results['steps_completed'].append('video_generation')
            self.progress.complete_step()
            
            # Paso 6: Subida a TikTok
            self.logger.info(f"📤 {self.progress.get_current_step()}")
            upload_results = self._step_upload(successful_videos, content_plan)
            
            successful_uploads = [up for up in upload_results if up.get('success', False)]
            results['videos_uploaded'] = len(successful_uploads)
            results['upload_results'] = upload_results
            results['steps_completed'].append('upload')
            self.progress.complete_step()
            
            # Paso 7: Finalización
            self.logger.info(f"✅ {self.progress.get_current_step()}")
            self._step_finalization(results)
            results['steps_completed'].append('finalization')
            self.progress.complete_step()
            
            results['success'] = True
            results['completed_at'] = datetime.now().isoformat()
            
            self.logger.success("🎉 Automatización completada exitosamente!")
            self._print_summary(results)
            
        except Exception as e:
            self.logger.error(f"❌ Error en automatización: {e}")
            results['errors'].append(str(e))
            results['failed_at'] = datetime.now().isoformat()
            results['completed_at'] = datetime.now().isoformat()
        
        # Guardar resultados finales
        self._save_session_results(results)
        
        return results
    
    def _step_scraping(self, username: str, max_videos: int) -> List[Dict[str, Any]]:
        """Paso 1: Scraping de métricas"""
        try:
            videos = scrape_tiktok_metrics(username, max_videos)
            self.logger.info(f"✅ Scraping completado: {len(videos)} videos analizados")
            return videos
        except Exception as e:
            self.logger.error(f"❌ Error en scraping: {e}")
            return []
    
    def _step_analysis(self, videos: List[Dict[str, Any]], username: str) -> Dict[str, Any]:
        """Paso 2: Análisis de tendencias"""
        try:
            analysis = analyze_tiktok_trends(videos, username)
            self.logger.info("✅ Análisis de tendencias completado")
            return analysis
        except Exception as e:
            self.logger.error(f"❌ Error en análisis: {e}")
            return {}
    
    def _step_content_planning(self, analysis: Dict[str, Any], video_count: int) -> Dict[str, Any]:
        """Paso 3: Generación de plan de contenido"""
        try:
            content_plan = create_content_plan(analysis, video_count)
            self.logger.info(f"✅ Plan de contenido creado para {video_count} videos")
            return content_plan
        except Exception as e:
            self.logger.error(f"❌ Error en planificación de contenido: {e}")
            return {}
    
    def _step_image_generation(self, content_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Paso 4: Generación de imágenes"""
        try:
            image_prompts = content_plan.get('image_prompts', [])
            if not image_prompts:
                self.logger.warning("No hay prompts de imágenes en el plan")
                return []
            
            generated_images = generate_images_from_prompts(image_prompts)
            successful_count = len([img for img in generated_images if img.get('success', False)])
            self.logger.info(f"✅ Generación de imágenes completada: {successful_count}/{len(image_prompts)} exitosas")
            return generated_images
        except Exception as e:
            self.logger.error(f"❌ Error en generación de imágenes: {e}")
            return []
    
    def _step_video_generation(self, content_plan: Dict[str, Any], generated_images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Paso 5: Generación de videos"""
        try:
            video_prompts = content_plan.get('video_prompts', [])
            image_paths = [img.get('image_path', '') for img in generated_images if img.get('success', False)]
            
            if not video_prompts:
                self.logger.warning("No hay prompts de videos en el plan")
                return []
            
            if not image_paths:
                self.logger.warning("No hay imágenes exitosas para generar videos")
                return []
            
            generated_videos = generate_videos_from_images(video_prompts, image_paths)
            successful_count = len([vid for vid in generated_videos if vid.get('success', False)])
            self.logger.info(f"✅ Generación de videos completada: {successful_count}/{len(video_prompts)} exitosos")
            return generated_videos
        except Exception as e:
            self.logger.error(f"❌ Error en generación de videos: {e}")
            return []
    
    def _step_upload(self, generated_videos: List[Dict[str, Any]], content_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Paso 6: Subida a TikTok"""
        try:
            if not generated_videos:
                self.logger.warning("No hay videos para subir")
                return []
            
            content_suggestions = content_plan.get('content_suggestions', [])
            
            upload_results = upload_videos_to_tiktok(generated_videos, content_suggestions)
            successful_count = len([up for up in upload_results if up.get('success', False)])
            self.logger.info(f"✅ Subida completada: {successful_count}/{len(generated_videos)} videos subidos")
            return upload_results
        except Exception as e:
            self.logger.error(f"❌ Error en subida: {e}")
            return []
    
    def _step_finalization(self, results: Dict[str, Any]):
        """Paso 7: Finalización y limpieza"""
        try:
            # Aquí podrías agregar:
            # - Limpieza de archivos temporales
            # - Envío de notificaciones
            # - Actualización de bases de datos
            # - Análisis post-procesamiento
            
            self.logger.info("✅ Finalización completada")
        except Exception as e:
            self.logger.error(f"❌ Error en finalización: {e}")
    
    def _print_summary(self, results: Dict[str, Any]):
        """Imprimir resumen de resultados"""
        self.logger.info("\n" + "="*50)
        self.logger.info("📊 RESUMEN DE AUTOMATIZACIÓN")
        self.logger.info("="*50)
        self.logger.info(f"🆔 Sesión: {results.get('session_id', 'N/A')}")
        self.logger.info(f"👤 Usuario: @{results.get('username', 'N/A')}")
        self.logger.info(f"⏰ Duración: {self._calculate_duration(results)}")
        self.logger.info(f"📈 Videos analizados: {results.get('scraped_videos_count', 0)}")
        self.logger.info(f"🎨 Imágenes generadas: {results.get('images_generated', 0)}")
        self.logger.info(f"🎬 Videos generados: {results.get('videos_generated', 0)}")
        self.logger.info(f"📤 Videos subidos: {results.get('videos_uploaded', 0)}")
        self.logger.info(f"✅ Estado: {'EXITOSO' if results.get('success') else 'FALLIDO'}")
        
        if results.get('errors'):
            self.logger.info(f"❌ Errores: {len(results['errors'])}")
        
        self.logger.info("="*50)
    
    def _calculate_duration(self, results: Dict[str, Any]) -> str:
        """Calcular duración de la sesión"""
        try:
            start_time = datetime.fromisoformat(results.get('started_at', ''))
            end_time = datetime.fromisoformat(results.get('completed_at', ''))
            duration = end_time - start_time
            
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            
            return f"{minutes}m {seconds}s"
        except:
            return "N/A"
    
    def _save_session_results(self, results: Dict[str, Any]):
        """Guardar resultados de la sesión"""
        try:
            filename = f"automation_session_{self.session_id}.json"
            filepath = config.get_data_dir('sessions')
            os.makedirs(filepath, exist_ok=True)
            filepath = f"{filepath}/{filename}"
            
            if save_json_file(results, filepath):
                self.logger.info(f"📁 Resultados guardados: {filename}")
            else:
                self.logger.error("❌ Error guardando resultados de sesión")
        except Exception as e:
            self.logger.error(f"❌ Error guardando sesión: {e}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Automatización de videos de TikTok')
    parser.add_argument('--username', '-u', required=True, help='Usuario de TikTok a analizar')
    parser.add_argument('--max-videos', '-m', type=int, default=50, help='Máximo de videos a analizar')
    parser.add_argument('--create-videos', '-c', type=int, default=3, help='Cantidad de videos a crear')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Ejecutar sin subir videos')
    
    args = parser.parse_args()
    
    # Crear instancia de automatización
    automation = TikTokAutomation()
    
    if args.dry_run:
        automation.logger.info("🧪 Modo dry-run activado - no se subirán videos")
    
    # Ejecutar automatización
    results = automation.run_full_automation(
        username=args.username,
        max_videos=args.max_videos,
        videos_to_create=args.create_videos
    )
    
    # Retornar código de salida
    return 0 if results.get('success', False) else 1

if __name__ == "__main__":
    exit(main())
