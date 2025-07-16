<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<div align="center">
  <img src="https://drive.google.com/file/d/12aZS8Tw9VPxAuVrjdzUd3hf3GaoSNIkY/view?usp=sharing" alt="Logo" width="120" />
  <h3 align="center">memomate</h3>
  <p align="center">
    👩‍💻 Ваш персональний бот-помічник для керування контактами та нотатками
    <br />
    <br />
    <a href="#about-the-project"><strong>Докладніше »</strong></a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Зміст</summary>
  <ol>
    <li><a href="#about-the-project">Про проєкт</a></li>
    <li><a href="#built-with">Технології</a></li>
    <li><a href="#features">Функціонал</a></li>
    <li><a href="#installation">Встановлення</a></li>
    <li><a href="#usage">Використання</a></li>
    <li><a href="#license">Ліцензія</a></li>
  </ol>
</details>

## 📌 Про проєкт

MemoMate — це консольний бот-помічник, який допомагає зберігати та керувати особистими контактами і нотатками. Він створений як тренувальний проєкт для закріплення знань Python, роботи з файлами та об'єктно-орієнтованого програмування.

Проєкт реалізує ключову ідею цифрового помічника, здатного:
- зберігати важливу інформацію
- структурувати записи
- полегшувати пошук потрібних даних

> Ми це зробили для Квітки, яка пише нотатки всюди та хоче навести з ними ладу🌸

<p align="right">(<a href="#readme-top">до початку</a>)</p>

---

## ⚙️ Технології

- Python 3.11
- Стандартна бібліотека (`datetime`, `re`, `os`, `json`)
- ООП + CLI інтерфейс

<p align="right">(<a href="#readme-top">до початку</a>)</p>

---

## 🚀 Основний функціонал

### Контакти:
- Додавання нових контактів (ім’я, телефон, email, адреса, день народження)
- Пошук за ім’ям
- Редагування, видалення записів
- Перевірка правильності введення телефону та email
- Вивід тих, у кого скоро день народження

### Нотатки:
- Створення текстових нотаток
- Пошук, редагування та видалення
- Додавання тегів
- Пошук за тегами

### Зберігання:
- Дані зберігаються у файлах (JSON)
- Витримує перезапуск - нічого не втрачається

<p align="right">(<a href="#readme-top">до початку</a>)</p>

---

## 📥 Встановлення

```bash
git clone https://github.com/univers-projects/project-memomate/
cd memomate
python main.py
```

<p align="right">(<a href="#readme-top">до початку</a>)</p>

---

## 🧑‍💻 Використання

Запустіть програму в терміналі. Далі — вводьте команди:

```plaintext
add contact John +380501112233 john@email.com Kyiv 1990-07-15
show birthdays 7
add note "Купити молоко" #покупки
search note #покупки
```

> Програма підкаже, яку команду можна обрати, просто почніть друкувати 😉

<p align="right">(<a href="#readme-top">до початку</a>)</p>

---

## 📄 Ліцензія

Використовуйте, як хочете — це навчальний проєкт 💙

<p align="right">(<a href="#readme-top">до початку</a>)</p>