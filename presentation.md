# Analīze

Lai aprēķinātu valūtas maiņas kursu, parasti ir jāveic trīs darbības: dodieties uz pārlūkprogrammu, 
ierakstiet konvertēšanas valūtas un simbolus un apstipriniet meklēšanu. Bet ko darīt, ja cilvēks nav tik pārliecināts 
par valūtas simboliem vai nezina, kā uzrakstīt tās nosaukumu?

# Specifikācija

Programmai jābūt telegrammas botam ar 3 pogām: konvertēšana, maiņas kursi un vēsture. Jāizmanto telethon bibliotēka (lai izveidotu robotu) un api.frankfurter.app API (lai iegūtu aktuālo informāciju par valūtas kursiem). Pirmajā palaišanas reizē (komanda /start) programmai jānosūta lietotājam apsveikuma ziņojums, kurā tiks stāstīts par bota funkcijām un pieejamajām komandām. Jābūt arī komandai /help, lai gadījumā, ja lietotājs var atcerēties, kādas komandas botam ir, atkal saņemot apsveikuma ziņojumu. Tagad atsevišķi par katru funkciju.

### Konvertēšana

Noklikšķinot uz šīs pogas, lietotājam būtu jānorāda, lai ievadītu valūtu, uz kuru tiks veikta konvertēšana, izmantojot pogas ar visām pieejamajām konvertēšanas valūtām un uzvedinošu paziņojumu.
Piemērs: "Uz kādu valūtu veiksiet konvertēšanu? <POGAS AR PIEEJAMAJĀM VALŪTĀM>...".

Pēc tam jāveic otrs līdzīgs ievades datu pieprasījums valūtai, KAS ir jāpārrēķina. Pēc tam konvertējamā summa jāpieprasa veselu skaitļu formātā ar atbilstošu pieprasījuma ziņojumu.
Piemērs: "Ievadiet konvertējamo summu...".

Pēc tam programmai jāatgriež konvertēšanas rezultāts ar visām izmantotajām valūtām un rezultātu.
Piemērs: "12 EUR ir 14,4 USD...".

### Valūtas maiņas kursi

Noklikšķinot uz šīs pogas, lietotājam jāredz aktuālā informācija par visu konvertēšanai pieejamo valūtu maiņas kursiem. Katram kursam jābūt parādītam attiecībā pret euro.
Piemērs: "Kurss: 1 USD = 1,1 EUR...".

### Vēsture

Noklikšķinot uz šīs pogas, lietotājam jāredz personīgā valūtas konvertāciju vēsture. 
Piemērs: "USD...".
Datu glabāšanai jāizmanto JSON fails. Visiem ziņojumiem jābūt rakstītiem angļu valodā un formatētiem ar emocijzīmēm.
(Piemērs: "🤝 Konvertēšana pabeigta...").

# Iterācijas

1. Frankfurt API
2. JSON data formati/glābšana
3. Bota UI konstruēšana
4. Ziņas formata dizains


# Izmantoti resursi!

- [Frankfurt API](https://api.frankfurter.app/)
- [Python JSON](https://www.w3schools.com/python/python_json.asp)
- [Telethon Documentation](https://docs.telethon.dev/en/stable/)
- [Python Requests Module](https://www.w3schools.com/python/module_requests.asp)
- [Get Emoji](https://getemoji.com/)
