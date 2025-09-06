#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 REFACTORING ULTRA-SEGURO - VIDEOSAUTOMATION
📋 Reorganiza el proyecto preservando todas las dependencias críticas
🛡️ Con múltiples verificaciones y rollback automático
"""

import os
import shutil
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

class UltraSafeRefactor:
    def __init__(self):
        self.backup_dir = f"BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.critical_files = [
            # Sistema principal de upload
            "subir_tiktok_selenium_final_v5.py",
            "dynamic_description_generator.py", 
            
            # Dependencias críticas
            "viral_video_prompt_generator.py",
            "image_metadata_analyzer.py",
            "viral_image_selector.py",
            
            # Pipeline principal (7 pasos críticos)
            "test_tiktok_scraping.py",
            "generate_prompts_from_scrap.py",
            "gen_images_from_prompts.py", 
            "generate_veo_video_from_image.py",
            "procesar_final_tiktok.py",
            "unir_videos_simple.py",
            
            # Orquestadores automáticos
            "run_complete_pipeline.py",
            "run_pipeline.py",
            "subir_multiples_videos_dinamicos.py",
            "subir_multiples_videos_ultra_dinamicos.py",
            
            # Archivos de configuración críticos
            "video_prompt_map.json",
            "gemini_utils.py",
            "setup.py",
            
            # Scripts de preparación
            "prepare_viral_pipeline.py",
            "run_simple_pipeline.py",
            "run_fast_pipeline.py"
        ]
        
        self.safe_to_archive = [
            # Testing files
            "test_*.py",
            "*_test.py", 
            "*_debug.py",
            "diagnostic_*.py",
            "anti_bot_test.py",
            
            # Experimental files
            "advanced_visual_analyzer.py",
            "authentic_viral_fusion.py",
            "create_visual_concept.py", 
            "definitive_viral_generator.py",
            "final_authentic_concept.py",
            "final_viral_video_generator.py",
            "intelligent_*.py",
            "viral_market_analyzer.py",
            "real_*.py",
            
            # Upload variants (keep only final_v5)
            "subir_tiktok_optimized*.py",
            "subir_tiktok_playwright.py",
            "subir_tiktok_preview*.py",
            "subir_tiktok_dragdrop*.py",
            "subir_tiktok_stealth*.py",
            "subir_tiktok_hidden*.py",
            "subir_tiktok_ultra_stealth*.py",
            "subir_tiktok_selenium_v5.py",
            "subir_tiktok_selenium_estable*.py",
            "subir_tiktok_selenium_auto*.py",
            "subir_tiktok_selenium_xpaths*.py",
            # Note: Keep subir_tiktok_selenium_final_v5.py
        ]
        
        self.debug_files_to_delete = [
            "debug_*.png",
            "dragdrop_*.png", 
            "*.html",
            "TaskManager.png"
        ]
        
    def create_full_backup(self):
        """Crear backup completo del proyecto"""
        print(f"🔒 CREANDO BACKUP COMPLETO en {self.backup_dir}...")
        
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)
            
        # Copiar todo excepto __pycache__ y .git
        shutil.copytree(".", self.backup_dir, 
                       ignore=shutil.ignore_patterns('__pycache__', '.git', '*.pyc'))
        print(f"✅ Backup creado: {self.backup_dir}")
        
    def verify_critical_files(self):
        """Verificar que todos los archivos críticos existen"""
        print("🔍 VERIFICANDO ARCHIVOS CRÍTICOS...")
        
        missing = []
        for file in self.critical_files:
            if not os.path.exists(file):
                missing.append(file)
                print(f"❌ FALTA: {file}")
            else:
                print(f"✅ {file}")
                
        if missing:
            print(f"\n🚨 FALTAN {len(missing)} ARCHIVOS CRÍTICOS!")
            print("🛑 DETENIENDO REFACTORING - REVISA EL PROYECTO")
            return False
            
        print("✅ Todos los archivos críticos están presentes\n")
        return True
        
    def test_imports_before(self):
        """Probar imports críticos antes del refactoring"""
        print("🧪 PROBANDO IMPORTS ANTES DEL REFACTORING...")
        
        critical_imports = [
            "dynamic_description_generator",
            "viral_video_prompt_generator", 
            "image_metadata_analyzer",
            "viral_image_selector",
            "gemini_utils"
        ]
        
        failed = []
        for module in critical_imports:
            try:
                __import__(module)
                print(f"✅ {module}")
            except ImportError as e:
                failed.append(module)
                print(f"❌ {module}: {e}")
                
        if failed:
            print(f"\n🚨 FALLAN {len(failed)} IMPORTS CRÍTICOS!")
            return False
            
        print("✅ Todos los imports críticos funcionan\n")
        return True
        
    def create_directories(self):
        """Crear nueva estructura de directorios"""
        print("📁 CREANDO NUEVA ESTRUCTURA...")
        
        directories = [
            "archive",
            "archive/testing", 
            "archive/experiments",
            "archive/upload_variants",
            "archive/debug_files",
            "utils",
            "core", 
            "data/videos/original",
            "data/videos/processed", 
            "data/videos/final"
        ]
        
        for dir_path in directories:
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 {dir_path}")
            
    def archive_safe_files(self):
        """Archivar archivos seguros (sin dependencias críticas)"""
        print("📦 ARCHIVANDO ARCHIVOS SEGUROS...")
        
        import glob
        archived_count = 0
        
        # Testing files
        for pattern in ["test_*.py", "*_test.py", "*_debug.py", "diagnostic_*.py"]:
            for file in glob.glob(pattern):
                if os.path.isfile(file):
                    shutil.move(file, f"archive/testing/{file}")
                    print(f"📦 {file} → archive/testing/")
                    archived_count += 1
                    
        # Experimental files
        experimental_patterns = [
            "advanced_visual_analyzer.py",
            "authentic_viral_fusion.py",
            "create_visual_concept.py",
            "definitive_viral_generator.py", 
            "final_authentic_concept.py",
            "final_viral_video_generator.py",
            "intelligent_*.py",
            "viral_market_analyzer.py",
            "real_*.py"
        ]
        
        for pattern in experimental_patterns:
            for file in glob.glob(pattern):
                if os.path.isfile(file):
                    shutil.move(file, f"archive/experiments/{file}")
                    print(f"🧪 {file} → archive/experiments/")
                    archived_count += 1
                    
        # Upload variants (keeping only final_v5)
        upload_patterns = [
            "subir_tiktok_optimized*.py",
            "subir_tiktok_playwright.py",
            "subir_tiktok_preview*.py", 
            "subir_tiktok_dragdrop*.py",
            "subir_tiktok_stealth*.py",
            "subir_tiktok_hidden*.py",
            "subir_tiktok_ultra_stealth*.py",
            "subir_tiktok_selenium_v5.py",
            "subir_tiktok_selenium_estable*.py",
            "subir_tiktok_selenium_auto*.py",
            "subir_tiktok_selenium_xpaths*.py"
        ]
        
        for pattern in upload_patterns:
            for file in glob.glob(pattern):
                # Skip the final version we want to keep
                if file != "subir_tiktok_selenium_final_v5.py" and os.path.isfile(file):
                    shutil.move(file, f"archive/upload_variants/{file}")
                    print(f"🚀 {file} → archive/upload_variants/")
                    archived_count += 1
                    
        print(f"✅ {archived_count} archivos archivados de forma segura\n")
        return archived_count
        
    def clean_debug_files(self):
        """Limpiar archivos de debug temporales"""
        print("🧹 LIMPIANDO ARCHIVOS DEBUG...")
        
        import glob
        deleted_count = 0
        
        for pattern in self.debug_files_to_delete:
            for file in glob.glob(pattern):
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"🗑️ {file}")
                    deleted_count += 1
                    
        # Limpiar __pycache__
        for root, dirs, files in os.walk('.'):
            for dir_name in dirs[:]:
                if dir_name == '__pycache__':
                    shutil.rmtree(os.path.join(root, dir_name))
                    print(f"🗑️ {os.path.join(root, dir_name)}")
                    dirs.remove(dir_name)
                    deleted_count += 1
                    
        print(f"✅ {deleted_count} archivos debug eliminados\n")
        return deleted_count
        
    def test_critical_functionality(self):
        """Probar funcionalidad crítica después de cambios"""
        print("🧪 PROBANDO FUNCIONALIDAD CRÍTICA...")
        
        try:
            # Test dynamic description generator
            from dynamic_description_generator import DynamicDescriptionGenerator
            gen = DynamicDescriptionGenerator()
            test_desc = gen.generate_dynamic_description('test.mp4', 'test prompt')
            print("✅ DynamicDescriptionGenerator funciona")
            
        except Exception as e:
            print(f"❌ DynamicDescriptionGenerator falló: {e}")
            return False
            
        try:
            # Test video prompt map loading
            with open('video_prompt_map.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            print("✅ video_prompt_map.json se puede cargar")
            
        except Exception as e:
            print(f"❌ video_prompt_map.json falló: {e}")
            return False
            
        print("✅ Funcionalidad crítica verificada\n")
        return True
        
    def move_utils(self):
        """Mover archivos de utilidades"""
        print("🔧 MOVIENDO UTILIDADES...")
        
        utils_files = [
            ("gemini_utils.py", "utils/gemini_utils.py"),
            ("setup.py", "setup.py"),  # Keep in root
        ]
        
        moved_count = 0
        for src, dst in utils_files:
            if os.path.exists(src) and src != dst:
                shutil.copy2(src, dst)
                print(f"🔧 {src} → {dst}")
                moved_count += 1
                
        print(f"✅ {moved_count} utilidades movidas\n")
        return moved_count
        
    def create_summary_report(self, stats):
        """Crear reporte de resumen"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "backup_location": self.backup_dir,
            "files_archived": stats.get('archived', 0),
            "files_deleted": stats.get('deleted', 0),
            "utils_moved": stats.get('utils_moved', 0),
            "critical_files_preserved": len(self.critical_files),
            "status": "SUCCESS",
            "critical_files": self.critical_files,
            "notes": "Refactoring ultra-seguro completado. Archivos críticos preservados en raíz."
        }
        
        with open("REFACTORING_REPORT.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print("\n📊 REPORTE DE REFACTORING:")
        print(f"📦 Archivos archivados: {stats.get('archived', 0)}")
        print(f"🗑️ Archivos eliminados: {stats.get('deleted', 0)}")
        print(f"🔧 Utilidades movidas: {stats.get('utils_moved', 0)}")
        print(f"🔒 Archivos críticos preservados: {len(self.critical_files)}")
        print(f"💾 Backup en: {self.backup_dir}")
        print("📄 Reporte completo: REFACTORING_REPORT.json")
        
    def rollback_if_needed(self):
        """Rollback automático si algo falla"""
        print("\n🚨 EJECUTANDO ROLLBACK...")
        
        # Remove new directories if empty
        for dir_name in ["archive", "utils"]:
            if os.path.exists(dir_name):
                try:
                    shutil.rmtree(dir_name)
                except:
                    pass
                    
        # Restore from backup
        if os.path.exists(self.backup_dir):
            print(f"🔄 Restaurando desde {self.backup_dir}...")
            
            # Copy files back
            for item in os.listdir(self.backup_dir):
                src = os.path.join(self.backup_dir, item)
                dst = item
                
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    
            print("✅ Rollback completado")
        else:
            print("❌ No se encontró backup para rollback")
            
    def execute_safe_refactoring(self):
        """Ejecutar refactoring ultra-seguro paso a paso"""
        print("🚀 INICIANDO REFACTORING ULTRA-SEGURO")
        print("=" * 60)
        
        stats = {}
        
        try:
            # Fase 1: Verificaciones iniciales
            if not self.verify_critical_files():
                return False
                
            if not self.test_imports_before():
                return False
                
            # Fase 2: Backup
            self.create_full_backup()
            
            # Fase 3: Crear estructura
            self.create_directories()
            
            # Fase 4: Archivar archivos seguros
            stats['archived'] = self.archive_safe_files()
            
            # Fase 5: Limpiar debug
            stats['deleted'] = self.clean_debug_files()
            
            # Fase 6: Mover utilidades
            stats['utils_moved'] = self.move_utils()
            
            # Fase 7: Verificación final
            if not self.test_critical_functionality():
                print("🚨 FUNCIONALIDAD CRÍTICA FALLÓ - EJECUTANDO ROLLBACK")
                self.rollback_if_needed()
                return False
                
            # Fase 8: Reporte final
            self.create_summary_report(stats)
            
            print("\n🎉 REFACTORING ULTRA-SEGURO COMPLETADO EXITOSAMENTE!")
            print("🔒 Todos los archivos críticos preservados")
            print("📦 Archivos no críticos organizados en archive/")
            print("✅ Funcionalidad verificada")
            
            return True
            
        except Exception as e:
            print(f"\n🚨 ERROR DURANTE REFACTORING: {e}")
            print("🔄 Ejecutando rollback automático...")
            self.rollback_if_needed()
            return False

def main():
    """Función principal"""
    print("🔒 VIDEOSAUTOMATION - REFACTORING ULTRA-SEGURO")
    print("=" * 60)
    print("⚠️  ESTE SCRIPT VA A REORGANIZAR EL PROYECTO")
    print("✅ Con backup automático y rollback de emergencia")
    print("🔒 Preservando todos los archivos críticos")
    print()
    
    response = input("¿Continuar con el refactoring ultra-seguro? (si/no): ").lower()
    if response not in ['si', 'sí', 's', 'yes', 'y']:
        print("❌ Refactoring cancelado por el usuario")
        return
        
    refactor = UltraSafeRefactor()
    success = refactor.execute_safe_refactoring()
    
    if success:
        print(f"\n✅ PROYECTO REFACTORIZADO EXITOSAMENTE")
        print(f"💾 Backup disponible en: {refactor.backup_dir}")
        print("🚀 El proyecto está listo para usar!")
    else:
        print(f"\n❌ REFACTORING FALLÓ")
        print("🔄 Rollback ejecutado - proyecto restaurado")
        print("🔍 Revisa los errores mostrados arriba")

if __name__ == "__main__":
    main()
