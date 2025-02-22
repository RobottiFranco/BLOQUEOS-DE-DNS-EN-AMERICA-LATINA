import os
import pandas as pd

categorias = {
    "ALDR": ["alcohol", "cerveza", "vino", "whisky", "drogas", "cannabis", "marihuana", "cocaína", "opio", "lsd", "mdma", "anfetamina", "heroína", "crack", "ketamina"],
    "REL": ["religión", "dios", "biblia", "corán", "iglesia", "mezquita", "templo", "budismo", "cristianismo", "islam", "hinduismo", "ateísmo", "teología", "rezar", "santo"],
    "PORN": ["porno", "pornografía", "xxx", "erótico", "adultos", "sex", "desnudo", "hardcore", "fetiche", "cams", "bdsm", "softcore", "hentai"],
    "PROV": ["bikini", "lingerie", "provocativo", "seductor", "modelo sexy", "atractivo", "exhibicionismo", "ropa ajustada"],
    "POLR": ["crítica política", "oposición", "anticorrupción", "democracia", "dictadura", "protesta", "reforma", "autoritarismo", "censura", "represión", "activismo", "patria"],
    "HUMR": ["derechos humanos", "feminismo", "igualdad", "justicia social", "minorías", "racismo", "discriminación", "género", "opresión", "abuso policial"],
    "ENV": ["medio ambiente", "deforestación", "contaminación", "cambio climático", "ecología", "reciclaje", "biodiversidad", "energíarenovable", "calentamientoglobal", "energia", "renovable"],
    "MILX": ["terrorismo", "separatistas", "yihad", "militante", "guerrilla", "radicalismo", "insurgencia", "extremismo", "conflicto armado", "atentado", "mil"],
    "HATE": ["odio", "racista", "homofobia", "misoginia", "antisemita", "supremacía", "discurso de odio", "xenofobia", "transfobia"],
    "NEWS": ["noticias", "cnn", "bbc", "periódico", "informativo", "diario", "noticiero", "actualidad", "reportaje", "medios de comunicación", "news"],
    "XED": ["educación sexual", "anticoncepción", "embarazo adolescente", "aborto", "salud sexual", "métodos anticonceptivos", "derechos reproductivos"],
    "PUBH": ["salud pública", "vih", "sars", "gripe aviar", "oms", "epidemia", "pandemia", "vacunas", "enfermedades infecciosas", "salud mental"],
    "GMB": ["casino", "apuestas", "poker", "lotería", "tragamonedas", "ruleta", "blackjack", "juego online", "jackpot", "bet", "match", "vegas", "play", "slots", "slot", "tombola", "juega", "juego", "gaming", "bingo", "gambling"],
    "ANON": ["vpn", "proxy", "tor", "anonimato", "elusión", "cifrado", "navegación privada", "darknet", "privacidad online"],
    "DATE": ["citas", "dating", "match", "pareja", "conocer gente", "relaciones", "aplicaciones de citas", "amor online"],
    "GRP": ["red social", "facebook", "twitter", "instagram", "tiktok", "linkedin", "foro", "grupo de discusión", "comunidad online"],
    "LGBT": ["lgbt", "gay", "lesbiana", "bisexual", "transexual", "queer", "pride", "identidad de género", "derechos lgbt"],
    "FILE": ["torrent", "descarga", "p2p", "compartir archivos", "mega", "drive", "cloud storage", "wetransfer"],
    "HACK": ["hacker", "seguridad informática", "ciberataque", "exploit", "pentesting", "ciberseguridad", "ransomware", "phishing"],
    "COMT": ["chat", "mensajería", "voip", "email", "whatsapp", "telegram", "foros", "IRC", "discord", "comunicación online"],
    "MMED": ["videos", "youtube", "spotify", "soundcloud", "fotografía", "streaming", "música online", "twitch"],
    "HOST": ["blog", "wordpress", "blogspot", "hosting", "plataforma de publicación", "sitios web", "dominios"],
    "SRCH": ["buscador", "google", "bing", "yahoo", "duckduckgo", "motor de búsqueda", "brave", "navegador", "chrome", "firefox"],
    "GAME": ["juego", "gamer", "videojuegos", "xbox", "playstation", "nintendo", "gaming", "steam", "esports", "play", "gaming"],
    "CULTR": ["historia", "cine", "música", "literatura", "humor", "entretenimiento", "arte", "teatro", "series"],
    "ECON": ["economía", "finanzas", "pobreza", "mercado", "desarrollo", "inversión", "crisis económica", "crisis","economica", "inflación"],
    "GOVT": ["gobierno", ".gob", "ministerio", "militar", "fuerzas armadas", "políticapública", "politica", "elecciones", "parlamento", "mil", "gov", "gob", "armada"],
    "COMM": ["ecommerce", "compra", "venta", "tienda online", "amazon", "mercadolibre", "shopify", "dropshipping"],
    "CTRL": ["contenido benigno", "control", "inocuo", "apto para todo público"],
    "IGO": ["onu", "unicef", "oms", "nacionesunidas", "intergubernamental", "bancomundial", "fmi"],
}


def definir_categoria(categorias: dict[str, list[str]], frase: str):
    categorias_detectadas = set()
    if isinstance(frase, str):
        frase = frase.lower()
        for codigo, palabras in categorias.items():
            if any(palabra in frase for palabra in palabras):
                categorias_detectadas.add(codigo)
    return list(categorias_detectadas) if categorias_detectadas else ["OTHER"]

directory = "src/data/comparative"

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)

        df = pd.read_csv(filepath)
        df['category'] = df['input'].apply(lambda x: ", ".join(definir_categoria(categorias, x)))
        df.to_csv(filepath, index=False)
