# Пример использования
## Размеры файлов
```
python tree.py --sizes
```

## Цветной вывод
```
python tree.py --color
```

## Всё вместе
```
python tree.py . --sizes --color
```

Только Python файлы
python tree.py --only py
Несколько расширений
python tree.py --only py,js,ts
Markdown экспорт
python tree.py --format md
Всё вместе
python tree.py . --only py --sizes --color --format md

Пример вывода (md)
project
├── src
│   ├── main.py
│   └── utils.py
├── data
└── README.md