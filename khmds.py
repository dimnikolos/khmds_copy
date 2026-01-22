import sys
import os
import re
import pypdf
import pyperclip
import winreg 
from ctypes import windll
try:
    from winotify import Notification
except ImportError:
    pass # Linux

# --- CONFIGURATION ---
MENU_NAME = "ΚΗΜΔΣ Αντιγραφή"  # Αυτό θα φαίνεται στο δεξί κλικ
CONTRACT_PATTERN = re.compile(r"\d{2}(REQ|AWRD|PROC|SYMV|PAY)\d+")

def show_message(title, msg, icon_type=0x40):
    """
    Εμφανίζει native Windows MessageBox.
    icon_type: 0x40 = Info, 0x10 = Error
    """
    # Χρησιμοποιούμε MessageBoxW για σωστή υποστήριξη Unicode/Ελληνικών
    windll.user32.MessageBoxW(0, msg, title, icon_type)

def register_context_menu():
    """
    Προσθέτει το πρόγραμμα στο δεξί κλικ του χρήστη (HKCU).
    ΔΕΝ χρειάζεται Admin Rights.
    """
    exe_path = os.path.abspath(sys.argv[0]) # Το path του .exe
    key_path = f"Software\\Classes\\SystemFileAssociations\\.pdf\\shell\\{MENU_NAME}"
    
    try:
        # 1. Δημιουργία του κλειδιού στο HKCU (User Registry)
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, MENU_NAME)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)

        # 2. Ορισμός της εντολής (Command)
        # Πρέπει να τρέξει μετά το pyinstaller (exe) και να μείνει το αρχείο σε αυτή τη θέση
        # είναι περιορισμός 

        command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command")
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
        winreg.CloseKey(command_key)
        
        show_message("Εγκατάσταση", f"Επιτυχία!\nΗ επιλογή '{MENU_NAME}' προστέθηκε στο δεξί κλικ.")
        
    except Exception as e:
        show_message("Σφάλμα", f"Δεν ήταν δυνατή η εγγραφή στο Registry:\n{e}", 0x10)

def extract_contract_id(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        if len(reader.pages) == 0: return None
        
        # Σάρωση 1ης σελίδας
        if "/Annots" in reader.pages[0]:
            for annot in reader.pages[0]["/Annots"]:
                annot_obj = annot.get_object()
                if "/AP" in annot_obj and "/N" in annot_obj["/AP"]:
                    ap_stream = annot_obj["/AP"]["/N"].get_object().get_data()
                    # Decode με ignore errors για τα binary σκουπίδια
                    text = ap_stream.decode('latin-1', errors='ignore')
                    match = CONTRACT_PATTERN.search(text)
                    if match:
                        return match.group(0)
    except Exception:
        return None
    return None

if __name__ == "__main__":
    # Σενάριο 1: Εγκατάσταση (Διπλό κλικ στο exe)
    if len(sys.argv) == 1:
        register_context_menu()
    
    # Σενάριο 2: Χρήση (Δεξί κλικ σε αρχείο -> το αρχείο έρχεται ως όρισμα)
    # ή αλλιώς python khmds.py file
    else:
        pdf_file = sys.argv[1]
        result = extract_contract_id(pdf_file)
        
        if result:
            pyperclip.copy(result)
            try:
                toast = Notification(
                    app_id= MENU_NAME,
                    title="Αντιγράφηκε!",
                    msg=f"Το {result} είναι στο πρόχειρο.",
                    duration="short",
                )
                toast.show()
            except NameError:
                # Fallback για Linux
                print(f"Αντιγράφηκε: {result}")
        else:
            try:
                toast = Notification(
                    app_id= MENU_NAME,
                    title="Αποτυχία!",
                    msg=f"Δεν βρέθηκε ΚΗΜΔΣ στο έγγραφο.",
                    duration="short",
                )
                toast.show()
            except NameError:
                # Fallback για Linux
                print(f"Δεν βρέθηκε ΚΗΜΔΣ στο έγγραφο.")