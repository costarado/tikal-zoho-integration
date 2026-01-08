# הוראות בעברית - Tikal API Integration

## ⚠ אזהרה: יש להגדיר api_key בקובץ config.py

קבל את api_key בעת התקנת ה-API במערכת Tikal.

## הגדרת API Key

1. פתח את הקובץ `config.py`
2. מצא את השורה: `'api_key': 'YOUR_API_KEY_HERE'`
3. החלף ב-API key האמיתי שלך:

```python
TIKAL_CONFIG = {
    'base_url': 'http://arielsip.com',
    'api_key': 'המפתח_האמיתי_שלך',  # החלף כאן
    'format': 'json',
}
```

## איך לקבל API Key

1. התקן את ה-API במערכת Tikal
2. בעת ההתקנה, תקבל "special key" - זהו ה-API key שלך
3. העתק את המפתח והדבק ב-`config.py`

## שימוש

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key']
)

# יצירת סוכן
agent = client.agents.create(
    agent_id='2012',
    name='bisly',
    password='1234'
)
```

## בעיות נפוצות

**שגיאה: Authentication failed**
- בדוק שה-API key נכון
- ודא שה-API מותקן ופעיל במערכת

**שגיאה: Connection error**
- בדוק שה-URL נכון
- ודא שהשרת זמין

## תמיכה

אם יש בעיות:
1. בדוק את ה-API key
2. ודא שה-API מותקן
3. בדוק את הלוגים

