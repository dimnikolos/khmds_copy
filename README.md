# ΚΗΜΔΣ Αντιγραφή

Ένα πρόγραμμα για Windows που αυτοματοποιεί την εξαγωγή κωδικών ΚΗΜΔΗΣ (ΑΔΑΜ) από PDF.

Σχεδιασμένο για να παρακάμπτει προβλήματα κωδικοποίησης (mojibake) σε σφραγίδες υπογραφών, διαβάζοντας απευθείας τα Raw Data του αρχείου.

![Icon](icon.ico) *(Το εικονίδιο της εφαρμογής)*

## 🚀 Δυνατότητες

* **Deep Stream Scanning:** Αναλύει το `Appearance Stream` (`/AP`) των Annotations, εντοπίζοντας IDs εκεί που το απλό Copy-Paste αποτυγχάνει.
* **PDF Context Menu Integration:** Εμφανίζεται **μόνο** όταν κάνετε δεξί κλικ σε αρχεία `.pdf` (μέσω `SystemFileAssociations`).
* **Native Windows Notifications:** Εμφανίζει μοντέρνα ειδοποίηση (Toast) με ήχο και εικονίδιο όταν βρεθεί και αντιγραφεί το ID.
* **Zero-Admin Installation:** Εγκαθίσταται στο προφίλ του χρήστη (`HKCU`) χωρίς να απαιτεί δικαιώματα Διαχειριστή (IT-friendly).
* **Smart Regex:** Αναγνωρίζει αυτόματα: `SYMV`, `PAY`, `REQ`, `AWRD`, `PROC`.

---

## 📦 Εγκατάσταση (Για τον Χρήστη)

Η εφαρμογή είναι portable και δεν απαιτεί σύνθετη εγκατάσταση. Εκτελέστε το αρχείο και μην το διαγράψετε.

1.  Κατεβάστε το εκτελέσιμο [εδώ](https://github.com/dimnikolos/khmds_copy/releases/download/khmds_copy/khmds.exe)

Αν θέλετε να αφαιρέσετε την επιλογή (γιατί;) κατεβάστε το uninstall:

2.  Κατεβάστε το uninstall [εδώ](https://github.com/dimnikolos/khmds_copy/releases/download/khmds_copy/uninstall.exe)
