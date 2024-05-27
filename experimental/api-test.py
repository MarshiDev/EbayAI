import requests

headers = {"Authorization": f"Bearer {open('hfapi.key', 'r').read()}"}
API_URL_QUESTION = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
API_URL_TRANSLATE = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-de-en"


def query(payload, api_url):
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 503:
        print("503: Model", api_url.split("/")[-1], "is booting up, retrying request...")
        response = requests.post(api_url, headers=headers, json=payload | {"options": {"wait_for_model": True}})
    if response.status_code == 404:
        print("404: Model", api_url.split("/")[-1], "is not reachable, returning empty dict.")
        return [{}]
    return response.json()


mb = """Apple MacBook Pro 14 Zoll 2023 512GB 16GB RAM M2 Pro Chip Space Grau Wie Neu

Wie Neu - 100% Akkukapazität - 7 Ladezyklen -

nur kleine Kratzer hinten am Apple Logo


Die Rechnung erfolgt auf Ihren Namen
Die Rechnung bei diesem Artikel erfolgt unter Verwendung der Differenzbesteuerung gemäß §25a UStG.
Sie erhalten eine Rechnung ohne ausgewiesene Umsatzsteuer
Die MwSt. ist entsprechend der Regelungen zur Differenzbesteuerung im Preis enthalten,allerdings ist ein Ausweis der Umsatzsteuer auf der Rechnung nicht möglich.




Lieferumfang:
Apple MacBook Pro, 96W USB-C Power Adapter, USB-C auf MagSafe 3 Kabel (2 m),
Dokumentation, Original Verpackung



Herstellergarantie:

Herstellergarantie bis 01.01.2025

Die Garantie Bedingungen des Herstellers finden Sie unter diesem Link (kopieren und in Browser einfügen):

Garantiebedingungen https://apple.co/2PkcQZo


Hinweis zur Gewährleistung: 
Ihre gesetzlichen Rechte gegen uns aus dem mit uns geschlossenen Kaufvertrag werden von diesem Garantieversprechen in keiner Weise eingeschränkt. Insbesondere etwaig bestehende gesetzliche Gewährleistungsrechte uns gegenüber bleiben von diesem Garantieversprechen unberührt.
Ist die Kaufsache mangelhaft, können Sie sich daher in jedem Fall an uns im Rahmen der gesetzlichen Gewährleistung halten, unabhängig davon, ob ein Garantiefall vorliegt oder die Garantie in Anspruch genommen wird.



Hinweise zur Batterieentsorgung
Im Zusammenhang mit dem Vertrieb von Batterien oder mit der Lieferung von Geräten, die Batterien enthalten, sind wir verpflichtet, Sie auf
folgendes hinzuweisen:
Sie sind zur Rückgabe gebrauchter Batterien als Endnutzer gesetzlich verpflichtet. Sie können Altbatterien, die wir als Neubatterien im
Sortiment führen oder geführt haben, unentgeltlich an unserem Versandlager (Versandadresse) zurückgeben. Die auf den Batterien
abgebildeten Symbole haben folgende Bedeutung:
Das Symbol der durchgekreuzten Mülltonne bedeutet, dass die Batterie nicht in den Hausmüll gegeben werden darf.
Pb = Batterie enthält mehr als 0,004 Masseprozent Blei
Cd = Batterie enthält mehr als 0,002 Masseprozent Cadmium
Hg = Batterie enthält mehr als 0,0005 Masseprozent Quecksilber.
Bitte beachten Sie die vorstehenden Hinweise."""
mb_short = query({"inputs": mb}, API_URL_TRANSLATE)[0].get("translation_text", "")
q = "Ist der artikel technisch einwandfrei, visuell keine Mängel?"
q_en = query({"inputs": q}, API_URL_TRANSLATE)[0].get("translation_text", "")
data = query({"inputs": {"question": q_en, "context": mb_short}}, API_URL_QUESTION)

print(data)
