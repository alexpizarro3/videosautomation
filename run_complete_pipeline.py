#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ORQUESTADOR COMPLETO DEL PIPELINE DE VIDEOS VIRALES
Ejecuta automáticamente todo el pipeline desde scraping hasta upload sin intervención humana
"""

import os
import sys
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

class CompletePipelineOrchestrator:
    """Orquestador completo del pipeline de videos virales"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.steps_completed = 0
        self.steps_failed = 0
        self.execution_log = []
        
        # Pipeline steps
        self.pipeline_steps = [
            {
                "id": 1,
                "name": "Extracción de Datos TikTok",
                "script": "test_tiktok_scraping.py",
                "timeout": 300,  # 5 minutos
                "required": True,
                "description": "Extrae datos y tendencias de TikTok"
            },
            {
                "id": 2,
                "name": "Generación de Prompts",
                "script": "generate_prompts_from_scrap.py",
                "timeout": 240,  # 4 minutos
                "required": True,
                "description": "Genera prompts creativos desde datos extraídos"
            },
            {
                "id": 3,
                "name": "Generación de Imágenes",
                "script": "gen_images_from_prompts.py",
                "timeout": 600,  # 10 minutos
                "required": True,
                "description": "Crea imágenes desde prompts generados"
            },
            {
                "id": 4,
                "name": "Generación de Videos",
                "script": "generate_veo_video_from_image.py",
                "timeout": 900,  # 15 minutos
                "required": True,
                "description": "Convierte imágenes en videos con Veo3"
            },
            {
                "id": 5,
                "name": "Procesamiento Final",
                "script": "procesar_final_tiktok.py",
                "timeout": 300,  # 5 minutos
                "required": True,
                "description": "Optimiza videos para TikTok"
            },
            {
                "id": 6,
                "name": "Unión de Videos",
                "script": "unir_videos_simple.py",
                "timeout": 180,  # 3 minutos
                "required": False,
                "description": "Une videos en uno final"
            },
            {
                "id": 7,
                "name": "Upload Dual TikTok + YouTube Shorts",
                "script": "dual_platform_uploader.py",
                "timeout": 1200,  # 20 minutos
                "required": True,
                "description": "Sube videos a TikTok y YouTube Shorts automáticamente"
            }
        ]
    
    def log_step(self, step_id: int, status: str, message: str, execution_time: float = 0):
        """Registra el resultado de un paso"""
        log_entry = {
            "step_id": step_id,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "message": message,
            "execution_time": execution_time
        }
        self.execution_log.append(log_entry)
        
        # Mostrar en consola
        status_emoji = "✅" if status == "SUCCESS" else "❌" if status == "ERROR" else "ℹ️"
        print(f"{status_emoji} Paso {step_id}: {message}")
        if execution_time > 0:
            print(f"   ⏱️ Tiempo: {execution_time:.1f}s")
    
    def execute_script(self, script_path: str, timeout: int) -> tuple[bool, str, float]:
        """
        Ejecuta un script de Python con timeout
        
        Returns:
            tuple: (success, output/error, execution_time)
        """
        if not os.path.exists(script_path):
            return False, f"Script no encontrado: {script_path}", 0
        
        start_time = time.time()
        
        try:
            # Ejecutar script con timeout
            result = subprocess.run(
                [sys.executable, script_path],
                timeout=timeout,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return True, result.stdout, execution_time
            else:
                return False, result.stderr or result.stdout, execution_time
                
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return False, f"Timeout después de {timeout}s", execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            return False, str(e), execution_time
    
    def check_prerequisites(self) -> bool:
        """Verifica que los prerequisitos estén listos"""
        print("🔍 Verificando prerequisitos del pipeline...")
        
        # Verificar archivos necesarios
        required_dirs = ["data", "config"]
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
                print(f"   📁 Creado directorio: {dir_name}")
        
        # Verificar scripts del pipeline
        missing_scripts = []
        for step in self.pipeline_steps:
            if not os.path.exists(step["script"]):
                missing_scripts.append(step["script"])
        
        if missing_scripts:
            print(f"❌ Scripts faltantes: {', '.join(missing_scripts)}")
            return False
        
        print("✅ Prerequisitos verificados")
        return True
    
    def execute_pipeline(self):
        """Ejecuta el pipeline completo"""
        print("🚀 INICIANDO PIPELINE COMPLETO DE VIDEOS VIRALES")
        print("=" * 60)
        print(f"⏰ Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Total de pasos: {len(self.pipeline_steps)}")
        print()
        
        # Verificar prerequisitos
        if not self.check_prerequisites():
            print("❌ No se pueden verificar los prerequisitos. Abortando.")
            return False
        
        # Ejecutar cada paso
        for step in self.pipeline_steps:
            step_start = time.time()
            
            print(f"\n📍 PASO {step['id']}/{len(self.pipeline_steps)}: {step['name']}")
            print(f"   🎯 {step['description']}")
            print(f"   📄 Ejecutando: {step['script']}")
            print(f"   ⏰ Timeout: {step['timeout']}s")
            
            # Ejecutar script
            success, output, execution_time = self.execute_script(step['script'], step['timeout'])
            
            if success:
                self.steps_completed += 1
                self.log_step(step['id'], "SUCCESS", f"{step['name']} completado", execution_time)
                
                # Mostrar output resumido si es exitoso
                if output and len(output.strip()) > 0:
                    lines = output.strip().split('\n')
                    if len(lines) > 5:
                        print(f"   📄 Output (últimas 3 líneas):")
                        for line in lines[-3:]:
                            print(f"      {line}")
                    else:
                        print(f"   📄 Output: {output.strip()}")
            else:
                self.steps_failed += 1
                self.log_step(step['id'], "ERROR", f"{step['name']} falló: {output}", execution_time)
                
                # Mostrar error
                print(f"   ❌ Error: {output}")
                
                # Si es un paso requerido, detener pipeline
                if step['required']:
                    print(f"\n❌ PIPELINE DETENIDO: Paso requerido {step['id']} falló")
                    break
                else:
                    print(f"   ⚠️ Paso opcional falló, continuando...")
        
        # Resumen final
        self.show_final_summary()
        
        # Guardar reporte
        self.save_execution_report()
        
        return self.steps_failed == 0
    
    def show_final_summary(self):
        """Muestra resumen final de la ejecución"""
        end_time = datetime.now()
        total_duration = end_time - self.start_time
        
        print("\n" + "=" * 60)
        print("🤖 RESUMEN FINAL DEL PIPELINE")
        print("=" * 60)
        print(f"⏱️ Duración total: {total_duration}")
        print(f"✅ Pasos completados: {self.steps_completed}/{len(self.pipeline_steps)}")
        print(f"❌ Pasos fallidos: {self.steps_failed}")
        
        success_rate = (self.steps_completed / len(self.pipeline_steps)) * 100
        print(f"📊 Tasa de éxito: {success_rate:.1f}%")
        
        if self.steps_failed == 0:
            print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
        elif self.steps_failed == len(self.pipeline_steps):
            print("💥 PIPELINE FALLÓ COMPLETAMENTE")
        else:
            print("⚠️ PIPELINE COMPLETADO CON ERRORES")
        
        print("=" * 60)
    
    def save_execution_report(self):
        """Guarda reporte detallado de la ejecución"""
        report = {
            "execution_info": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_duration": str(datetime.now() - self.start_time),
                "steps_completed": self.steps_completed,
                "steps_failed": self.steps_failed,
                "success_rate": (self.steps_completed / len(self.pipeline_steps)) * 100
            },
            "pipeline_steps": self.pipeline_steps,
            "execution_log": self.execution_log
        }
        
        timestamp = int(time.time())
        report_file = f"pipeline_complete_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Reporte guardado: {report_file}")

def main():
    """Función principal"""
    print("🤖 ORQUESTADOR COMPLETO DE PIPELINE DE VIDEOS VIRALES")
    print("🎯 Ejecuta automáticamente todo el proceso sin intervención humana")
    print()
    
    # Confirmar ejecución
    print("⚠️ IMPORTANTE: Este proceso puede tomar 45-60 minutos en completarse")
    print("📝 Se ejecutarán automáticamente:")
    print("   1. Scraping de TikTok")
    print("   2. Generación de prompts")
    print("   3. Generación de imágenes")
    print("   4. Generación de videos")
    print("   5. Procesamiento final")
    print("   6. Unión de videos")
    print("   7. Upload automatizado")
    print()
    
    # Opción de cancelar
    try:
        print("Presiona Ctrl+C en los próximos 10 segundos para cancelar...")
        time.sleep(10)
    except KeyboardInterrupt:
        print("\n❌ Ejecución cancelada por el usuario")
        return
    
    # Ejecutar pipeline
    orchestrator = CompletePipelineOrchestrator()
    success = orchestrator.execute_pipeline()
    
    # Exit code para scripts automatizados
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
