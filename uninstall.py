import winreg
from ctypes import windll

# Το όνομα που είχαμε ορίσει στο κυρίως script
MENU_NAME = "ΚΗΜΔΣ Αντιγραφή"
REG_PATH = f"Software\\Classes\\SystemFileAssociations\\.pdf\\shell"

def uninstall_context_menu():
    try:
        # Ανοίγουμε το κλειδί "parent" (εκεί που βρίσκονται όλα τα shell extensions)
        # HKEY_CURRENT_USER\Software\Classes\*\shell
        parent_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        
        # 1. Προσπάθεια διαγραφής του υπο-κλειδιού "command"
        # Πρέπει να σβηστεί πρώτα αυτό, αλλιώς δεν σβήνεται ο φάκελος "Αντιγραφή ΚΗΜΔΣ"
        try:
            winreg.DeleteKey(parent_key, f"{MENU_NAME}\\command")
        except FileNotFoundError:
            pass # Αν δεν υπάρχει, προχωράμε
            
        # 2. Προσπάθεια διαγραφής του κυρίως φακέλου "ΚΗΜΔΣ Αντιγραφή"
        winreg.DeleteKey(parent_key, MENU_NAME)
        
        winreg.CloseKey(parent_key)
        
        windll.user32.MessageBoxW(0, f"Η επιλογή '{MENU_NAME}' αφαιρέθηκε επιτυχώς από το μενού.", "Απεγκατάσταση", 0x40)
        
    except FileNotFoundError:
        windll.user32.MessageBoxW(0, "Η εφαρμογή δεν βρέθηκε στο Registry.\nΊσως έχει ήδη απεγκατασταθεί.", "Πληροφορία", 0x40)
    except Exception as e:
        windll.user32.MessageBoxW(0, f"Σφάλμα κατά την απεγκατάσταση:\n{e}", "Σφάλμα", 0x10)

if __name__ == "__main__":
    uninstall_context_menu()