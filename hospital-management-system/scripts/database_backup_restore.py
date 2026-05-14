import sqlite3
import os
import shutil
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_path='hospital_management.db'):
        self.db_path = db_path
        self.backup_dir = 'backups'
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """Create a backup of the current database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"hospital_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copy the database file
            shutil.copy2(self.db_path, backup_path)
            
            # Create backup info file
            info = {
                'backup_date': datetime.now().isoformat(),
                'original_db': self.db_path,
                'backup_file': backup_filename,
                'file_size': os.path.getsize(backup_path)
            }
            
            info_path = os.path.join(self.backup_dir, f"backup_info_{timestamp}.json")
            with open(info_path, 'w') as f:
                json.dump(info, f, indent=2)
            
            print(f"[v0] Backup created successfully: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"[v0] Error creating backup: {str(e)}")
            return None
    
    def restore_backup(self, backup_path):
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                print(f"[v0] Backup file not found: {backup_path}")
                return False
            
            # Create backup of current database before restore
            current_backup = self.create_backup()
            if current_backup:
                print(f"[v0] Current database backed up before restore")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            print(f"[v0] Database restored successfully from: {backup_path}")
            return True
            
        except Exception as e:
            print(f"[v0] Error restoring backup: {str(e)}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        try:
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('hospital_backup_') and filename.endswith('.db'):
                    backup_path = os.path.join(self.backup_dir, filename)
                    info_file = filename.replace('.db', '.json').replace('hospital_backup_', 'backup_info_')
                    info_path = os.path.join(self.backup_dir, info_file)
                    
                    backup_info = {
                        'filename': filename,
                        'path': backup_path,
                        'size': os.path.getsize(backup_path),
                        'created': datetime.fromtimestamp(os.path.getctime(backup_path))
                    }
                    
                    # Load additional info if available
                    if os.path.exists(info_path):
                        with open(info_path, 'r') as f:
                            additional_info = json.load(f)
                            backup_info.update(additional_info)
                    
                    backups.append(backup_info)
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            print(f"[v0] Found {len(backups)} backup(s):")
            for i, backup in enumerate(backups, 1):
                print(f"  {i}. {backup['filename']}")
                print(f"     Created: {backup['created']}")
                print(f"     Size: {backup['size']} bytes")
                print()
            
            return backups
            
        except Exception as e:
            print(f"[v0] Error listing backups: {str(e)}")
            return []
    
    def cleanup_old_backups(self, keep_count=5):
        """Keep only the most recent backups"""
        try:
            backups = self.list_backups()
            
            if len(backups) <= keep_count:
                print(f"[v0] No cleanup needed. Current backups: {len(backups)}, Keep: {keep_count}")
                return
            
            # Remove old backups
            backups_to_remove = backups[keep_count:]
            
            for backup in backups_to_remove:
                try:
                    os.remove(backup['path'])
                    
                    # Remove info file if exists
                    info_file = backup['filename'].replace('.db', '.json').replace('hospital_backup_', 'backup_info_')
                    info_path = os.path.join(self.backup_dir, info_file)
                    if os.path.exists(info_path):
                        os.remove(info_path)
                    
                    print(f"[v0] Removed old backup: {backup['filename']}")
                    
                except Exception as e:
                    print(f"[v0] Error removing backup {backup['filename']}: {str(e)}")
            
            print(f"[v0] Cleanup completed. Kept {keep_count} most recent backups.")
            
        except Exception as e:
            print(f"[v0] Error during cleanup: {str(e)}")
    
    def verify_database_integrity(self):
        """Verify database integrity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Run integrity check
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            if result[0] == 'ok':
                print("[v0] Database integrity check: PASSED")
                
                # Get database statistics
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                print(f"[v0] Database contains {len(tables)} tables:")
                
                total_records = 0
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    total_records += count
                    print(f"  - {table_name}: {count} records")
                
                print(f"[v0] Total records in database: {total_records}")
                
            else:
                print(f"[v0] Database integrity check: FAILED - {result[0]}")
            
            conn.close()
            return result[0] == 'ok'
            
        except Exception as e:
            print(f"[v0] Error verifying database integrity: {str(e)}")
            return False

def main():
    """Main function to demonstrate database management"""
    print("[v0] Hospital Management System - Database Manager")
    print("=" * 50)
    
    db_manager = DatabaseManager()
    
    # Verify current database
    print("\n1. Verifying current database integrity...")
    db_manager.verify_database_integrity()
    
    # Create backup
    print("\n2. Creating database backup...")
    backup_path = db_manager.create_backup()
    
    # List all backups
    print("\n3. Listing all available backups...")
    backups = db_manager.list_backups()
    
    # Cleanup old backups (keep only 3 most recent)
    print("\n4. Cleaning up old backups...")
    db_manager.cleanup_old_backups(keep_count=3)
    
    print("\n[v0] Database management operations completed successfully!")

if __name__ == "__main__":
    main()
