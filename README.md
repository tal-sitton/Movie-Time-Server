# Movie Time (Server)
[לאפליקציה עצמה](https://github.com/tal-sitton/Movie-Time/tree/add-readme#movie-time)

בעזרת האפליקציה, תוכלו לראות אילו סרטים מוצגים באילו בתי קולנוע, בקלות וביעילות.

## השרת
השרת כל יום (בחמש/שש בבוקר) מתעדכן עם האתרים של בתי הקולנוע ורואה מתי מוקרן איזה סרט ובאיזה בית קולנוע.

הוא עושה זאת בעזרת request לאתרים של בתי הקולנוע.

השרת כתוב בשפת python, והתוצאות שהוא מוצא על הסרטים נשמרים [בצורת קובץ JSON](movies.json)

---

[To the app itself](https://github.com/tal-sitton/Movie-Time/tree/add-readme#movie-time)

Using the app, you can see which cinema shows what movies.

## The Server
Every day, the server gathers information using the cinema's websites about what movies show in each cinema.

It uses the requests module to gather the info.

The server is written in python, and the data is saved in a [JSON file](movies.json)
