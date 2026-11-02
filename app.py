import json
import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = os.environ.get(
    "DB_PATH", os.path.join(os.path.dirname(__file__), "botequim_caico.db")
)

MENU_ITEMS = [
    # Espetinhos (Todos acompanham farofa crocante na manteiga da terra e vinagrete no prato preto tradicional!)
    {
        "id": 1,
        "nome": "Alcatra",
        "categoria": "espetinhos",
        "preco": 14.99,
        "destaque": True,
        "selo": "Especial da Brasa",
        "descricao": "Espetinho de alcatra macia e suculenta assada na brasa. Acompanha farofa crocante e vinagrete.",
        "icone": "🥩",
        "acompanha_farofa": True,
    },
    {
        "id": 2,
        "nome": "Carne",
        "categoria": "espetinhos",
        "preco": 10.99,
        "destaque": False,
        "selo": "Tradicional",
        "descricao": "Espetinho de carne bovina temperada no capricho e assada na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍢",
        "acompanha_farofa": True,
    },
    {
        "id": 3,
        "nome": "Carne com Bacon",
        "categoria": "espetinhos",
        "preco": 12.99,
        "destaque": True,
        "selo": "Muito Pedido",
        "descricao": "Cubos de carne bovina envoltos em bacon defumado crocante na brasa. Acompanha farofa e vinagrete.",
        "icone": "🥓",
        "acompanha_farofa": True,
    },
    {
        "id": 4,
        "nome": "Cupim",
        "categoria": "espetinhos",
        "preco": 11.99,
        "destaque": False,
        "selo": "Macio & Suculento",
        "descricao": "Cupim macio, bem assadinho na brasa com manteiga da terra. Acompanha farofa e vinagrete.",
        "icone": "🥩",
        "acompanha_farofa": True,
    },
    {
        "id": 5,
        "nome": "Carne de Sol com Queijo",
        "categoria": "espetinhos",
        "preco": 12.99,
        "destaque": True,
        "selo": "Sabor de Caicó",
        "descricao": "Legítima carne de sol combinada com queijo coalho tostado na brasa. Acompanha farofa e vinagrete.",
        "icone": "🧀",
        "acompanha_farofa": True,
    },
    {
        "id": 6,
        "nome": "Charque",
        "categoria": "espetinhos",
        "preco": 12.99,
        "destaque": False,
        "selo": "Raiz do Sertão",
        "descricao": "Charque selecionada e dessalgada no ponto certo, assada na brasa. Acompanha farofa e vinagrete.",
        "icone": "🥩",
        "acompanha_farofa": True,
    },
    {
        "id": 7,
        "nome": "Coração",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Clássico de Boteco",
        "descricao": "Coraçãozinho de frango temperado e bem assadinho na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍢",
        "acompanha_farofa": True,
    },
    {
        "id": 8,
        "nome": "Calabresa",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Na Brasa",
        "descricao": "Calabresa defumada assada na brasa até dourar. Acompanha farofa e vinagrete.",
        "icone": "🌭",
        "acompanha_farofa": True,
    },
    {
        "id": 9,
        "nome": "Calabresa com Queijo",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Combinação Perfeita",
        "descricao": "Espetinho de calabresa defumada intercalada com queijo coalho na brasa. Acompanha farofa e vinagrete.",
        "icone": "🧀",
        "acompanha_farofa": True,
    },
    {
        "id": 10,
        "nome": "Calabresa com Frango",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Misto na Brasa",
        "descricao": "Combinação suculenta de calabresa com cubos de frango temperado. Acompanha farofa e vinagrete.",
        "icone": "🍢",
        "acompanha_farofa": True,
    },
    {
        "id": 11,
        "nome": "Frango",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Bem Temperado",
        "descricao": "Cubos de frango marinados no tempero da casa e assados na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍗",
        "acompanha_farofa": True,
    },
    {
        "id": 12,
        "nome": "Frango com Bacon",
        "categoria": "espetinhos",
        "preco": 11.99,
        "destaque": True,
        "selo": "Suculento",
        "descricao": "Medalhão de frango temperado envolto em fatias de bacon crocante. Acompanha farofa e vinagrete.",
        "icone": "🥓",
        "acompanha_farofa": True,
    },
    {
        "id": 13,
        "nome": "Kafta de Charque c/ Queijo",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": True,
        "selo": "Especial da Casa",
        "descricao": "Kafta artesanal de charque recheada com queijo coalho derretido na brasa. Acompanha farofa e vinagrete.",
        "icone": "🔥",
        "acompanha_farofa": True,
    },
    {
        "id": 14,
        "nome": "Kafta de Carneiro",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Sabor Regional",
        "descricao": "Kafta de carneiro temperada com ervas e especiarias na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍢",
        "acompanha_farofa": True,
    },
    {
        "id": 15,
        "nome": "Kafta Bovina c/ Queijo",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Recheada",
        "descricao": "Kafta bovina suculenta com queijo coalho na brasa viva. Acompanha farofa e vinagrete.",
        "icone": "🧀",
        "acompanha_farofa": True,
    },
    {
        "id": 16,
        "nome": "Linguiça Toscana",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Bem Assadinha",
        "descricao": "Linguiça toscana suculenta assada na brasa até dourar. Acompanha farofa e vinagrete.",
        "icone": "🌭",
        "acompanha_farofa": True,
    },
    {
        "id": 17,
        "nome": "Moela",
        "categoria": "espetinhos",
        "preco": 6.99,
        "destaque": False,
        "selo": "Petisco Raiz",
        "descricao": "Moela macia e bem temperada, assada no ponto certo na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍢",
        "acompanha_farofa": True,
    },
    {
        "id": 18,
        "nome": "Maminha",
        "categoria": "espetinhos",
        "preco": 12.99,
        "destaque": True,
        "selo": "Corte Nobre",
        "descricao": "Tiras macias de maminha assadas na brasa com manteiga do sertão. Acompanha farofa e vinagrete.",
        "icone": "🥩",
        "acompanha_farofa": True,
    },
    {
        "id": 19,
        "nome": "Ovo com Bacon",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Irresistível",
        "descricao": "Ovos de codorna/galinha envoltos em bacon defumado tostado na brasa. Acompanha farofa e vinagrete.",
        "icone": "🥓",
        "acompanha_farofa": True,
    },
    {
        "id": 20,
        "nome": "Pão de Alho",
        "categoria": "espetinhos",
        "preco": 7.99,
        "destaque": False,
        "selo": "Bem Douradinho",
        "descricao": "Pão de alho crocante por fora e super cremoso por dentro, tostado na brasa.",
        "icone": "🥖",
        "acompanha_farofa": False,
    },
    {
        "id": 21,
        "nome": "Picanha",
        "categoria": "espetinhos",
        "preco": 15.99,
        "destaque": True,
        "selo": "Campeão Premium",
        "descricao": "Picanha bovina macia com gordurinha dourada na brasa. Acompanha farofa crocante e vinagrete.",
        "icone": "🔥",
        "acompanha_farofa": True,
    },
    {
        "id": 22,
        "nome": "Picanha Suína",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Saborosa",
        "descricao": "Picanha suína temperada e assada no ponto certo na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍖",
        "acompanha_farofa": True,
    },
    {
        "id": 23,
        "nome": "Porco",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Na Brasa",
        "descricao": "Espetinho de carne suína macia e bem temperada na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍖",
        "acompanha_farofa": True,
    },
    {
        "id": 24,
        "nome": "Queijo Coalho",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Tradição de Caicó",
        "descricao": "Queijo coalho legítimo tostado nos quatro lados na brasa viva.",
        "icone": "🧀",
        "acompanha_farofa": False,
    },
    {
        "id": 25,
        "nome": "Queijo com Orégano",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Aromático",
        "descricao": "Queijo coalho assado na brasa e finalizado com toque especial de orégano.",
        "icone": "🧀",
        "acompanha_farofa": False,
    },
    {
        "id": 26,
        "nome": "Queijo com Mel",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": True,
        "selo": "Clássico do Seridó",
        "descricao": "Queijo coalho dourado na brasa finalizado com fio generoso de mel de engenho.",
        "icone": "🍯",
        "acompanha_farofa": False,
    },
    {
        "id": 27,
        "nome": "Romeu e Julieta c/ Bacon",
        "categoria": "espetinhos",
        "preco": 12.99,
        "destaque": True,
        "selo": "Agridoce na Brasa",
        "descricao": "Combinação irresistível de queijo e goiabada envoltos em bacon crocante na brasa.",
        "icone": "🥓",
        "acompanha_farofa": False,
    },
    {
        "id": 28,
        "nome": "Tulipa",
        "categoria": "espetinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "Bem Crocante",
        "descricao": "Tulipas de frango temperadas e assadas até ficarem douradinhas na brasa. Acompanha farofa e vinagrete.",
        "icone": "🍗",
        "acompanha_farofa": True,
    },
    {
        "id": 29,
        "nome": "Salsichão",
        "categoria": "espetinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "Clássico",
        "descricao": "Salsichão assado na brasa no ponto certo. Acompanha farofa e vinagrete.",
        "icone": "🌭",
        "acompanha_farofa": True,
    },
    # Porções
    {
        "id": 30,
        "nome": "Macaxeira Cozida 300g",
        "categoria": "porcoes",
        "preco": 9.99,
        "destaque": False,
        "selo": "Porção 300g",
        "descricao": "Porção de macaxeira cozida macia, finalizada na manteiga da terra.",
        "icone": "🥔",
        "acompanha_farofa": False,
    },
    {
        "id": 31,
        "nome": "Macaxeira Frita 300g",
        "categoria": "porcoes",
        "preco": 9.99,
        "destaque": False,
        "selo": "Crocante 300g",
        "descricao": "Porção de macaxeira frita douradinha e crocante por fora, macia por dentro.",
        "icone": "🍟",
        "acompanha_farofa": False,
    },
    {
        "id": 32,
        "nome": "Purê de Macaxeira",
        "categoria": "porcoes",
        "preco": 19.99,
        "destaque": True,
        "selo": "Especial da Casa",
        "descricao": "Purê cremoso de macaxeira. Sabores: Carne de Sol, Calabresa ou Charque.",
        "icone": "🍲",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o sabor do Purê:",
        "opcoes": [
            {"valor": "Sabor: Carne de Sol", "label": "🥩 Carne de Sol", "preco": 19.99},
            {"valor": "Sabor: Calabresa", "label": "🌭 Calabresa", "preco": 19.99},
            {"valor": "Sabor: Charque", "label": "🥩 Charque", "preco": 19.99},
        ],
    },
    {
        "id": 33,
        "nome": "Rubacão",
        "categoria": "porcoes",
        "preco": 20.99,
        "destaque": True,
        "selo": "Tradição Nordestina",
        "descricao": "Rubacão caprichado e cremoso. Sabores: Calabresa, Carne de Sol ou Charque.",
        "icone": "🍛",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o sabor do Rubacão:",
        "opcoes": [
            {"valor": "Sabor: Calabresa", "label": "🌭 Calabresa", "preco": 20.99},
            {"valor": "Sabor: Carne de Sol", "label": "🥩 Carne de Sol", "preco": 20.99},
            {"valor": "Sabor: Charque", "label": "🥩 Charque", "preco": 20.99},
        ],
    },
    {
        "id": 34,
        "nome": "Batata Frita 300g",
        "categoria": "porcoes",
        "preco": 14.99,
        "destaque": False,
        "selo": "Porção 300g",
        "descricao": "Porção de batata frita sequinha e crocante (300g).",
        "icone": "🍟",
        "acompanha_farofa": False,
    },
    {
        "id": 35,
        "nome": "Tripa",
        "categoria": "porcoes",
        "preco": 15.99,
        "destaque": False,
        "selo": "Tira-Gosto Raiz",
        "descricao": "Porção de tripa bem torradinha e temperada no capricho.",
        "icone": "🍖",
        "acompanha_farofa": False,
    },
    {
        "id": 36,
        "nome": "Arroz",
        "categoria": "porcoes",
        "preco": 6.99,
        "destaque": False,
        "selo": "Guarnição",
        "descricao": "Porção de arroz soltinho e quentinho para acompanhar seu pedido.",
        "icone": "🍚",
        "acompanha_farofa": False,
    },
    # Caldinhos
    {
        "id": 37,
        "nome": "Caldinho Cabeça de Galo",
        "categoria": "caldinhos",
        "preco": 7.99,
        "destaque": True,
        "selo": "P: R$ 7,99 • G: R$ 11,99",
        "descricao": "Caldinho tradicional de cabeça de galo bem temperado e quentinho.",
        "icone": "🥣",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o tamanho:",
        "opcoes": [
            {"valor": "Tamanho P", "label": "🥣 Tamanho P — R$ 7,99", "preco": 7.99},
            {"valor": "Tamanho G", "label": "🍲 Tamanho G — R$ 11,99", "preco": 11.99},
        ],
    },
    {
        "id": 38,
        "nome": "Caldinho de Mocotó",
        "categoria": "caldinhos",
        "preco": 8.99,
        "destaque": True,
        "selo": "P: R$ 8,99 • G: R$ 12,99",
        "descricao": "Caldinho de mocotó encorpado e cheio de sabor.",
        "icone": "🥣",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o tamanho:",
        "opcoes": [
            {"valor": "Tamanho P", "label": "🥣 Tamanho P — R$ 8,99", "preco": 8.99},
            {"valor": "Tamanho G", "label": "🍲 Tamanho G — R$ 12,99", "preco": 12.99},
        ],
    },
    {
        "id": 39,
        "nome": "Caldinho de Peixe",
        "categoria": "caldinhos",
        "preco": 8.99,
        "destaque": False,
        "selo": "P: R$ 8,99 • G: R$ 12,99",
        "descricao": "Caldinho cremoso de peixe temperado com cheiro-verde.",
        "icone": "🐟",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o tamanho:",
        "opcoes": [
            {"valor": "Tamanho P", "label": "🥣 Tamanho P — R$ 8,99", "preco": 8.99},
            {"valor": "Tamanho G", "label": "🍲 Tamanho G — R$ 12,99", "preco": 12.99},
        ],
    },
    {
        "id": 40,
        "nome": "Caldinho de Camarão",
        "categoria": "caldinhos",
        "preco": 10.99,
        "destaque": True,
        "selo": "P: R$ 10,99 • G: R$ 14,99",
        "descricao": "Caldinho especial de camarão super cremoso e saboroso.",
        "icone": "🦐",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o tamanho:",
        "opcoes": [
            {"valor": "Tamanho P", "label": "🥣 Tamanho P — R$ 10,99", "preco": 10.99},
            {"valor": "Tamanho G", "label": "🍲 Tamanho G — R$ 14,99", "preco": 14.99},
        ],
    },
    {
        "id": 41,
        "nome": "Caldinho de Marisco",
        "categoria": "caldinhos",
        "preco": 9.99,
        "destaque": False,
        "selo": "P: R$ 9,99 • G: R$ 13,99",
        "descricao": "Caldinho de marisco quentinho e bem temperado no capricho.",
        "icone": "🦪",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o tamanho:",
        "opcoes": [
            {"valor": "Tamanho P", "label": "🥣 Tamanho P — R$ 9,99", "preco": 9.99},
            {"valor": "Tamanho G", "label": "🍲 Tamanho G — R$ 13,99", "preco": 13.99},
        ],
    },
    # Jantas
    {
        "id": 42,
        "nome": "Cuscuz Recheado",
        "categoria": "jantas",
        "preco": 19.99,
        "destaque": True,
        "selo": "Janta Nordestina",
        "descricao": "Cuscuz fofinho e bem recheado. Sabores: Carne de Sol, Calabresa, Frango ou Carne ao Molho.",
        "icone": "🌽",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o sabor do Cuscuz:",
        "opcoes": [
            {"valor": "Sabor: Carne de Sol", "label": "🥩 Carne de Sol", "preco": 19.99},
            {"valor": "Sabor: Calabresa", "label": "🌭 Calabresa", "preco": 19.99},
            {"valor": "Sabor: Frango", "label": "🍗 Frango", "preco": 19.99},
            {"valor": "Sabor: Carne ao Molho", "label": "🍲 Carne ao Molho", "preco": 19.99},
        ],
    },
    {
        "id": 43,
        "nome": "Macaxeira Completa",
        "categoria": "jantas",
        "preco": 19.99,
        "destaque": True,
        "selo": "Janta Regional",
        "descricao": "Macaxeira macia servida com acompanhamento especial. Sabores: Carne de Sol, Calabresa, Frango ou Carne ao Molho.",
        "icone": "🍽️",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o sabor da Macaxeira:",
        "opcoes": [
            {"valor": "Sabor: Carne de Sol", "label": "🥩 Carne de Sol", "preco": 19.99},
            {"valor": "Sabor: Calabresa", "label": "🌭 Calabresa", "preco": 19.99},
            {"valor": "Sabor: Frango", "label": "🍗 Frango", "preco": 19.99},
            {"valor": "Sabor: Carne ao Molho", "label": "🍲 Carne ao Molho", "preco": 19.99},
        ],
    },
    {
        "id": 44,
        "nome": "Sopa",
        "categoria": "jantas",
        "preco": 9.99,
        "destaque": False,
        "selo": "Caseira & Quentinha",
        "descricao": "Sopa caseira quentinha e bem temperada feita no capricho.",
        "icone": "🍲",
        "acompanha_farofa": False,
    },
    # Bebidas
    {
        "id": 45,
        "nome": "Água Mineral s/ Gás",
        "categoria": "bebidas",
        "preco": 2.99,
        "destaque": False,
        "selo": "Geladinha",
        "descricao": "Garrafa de água mineral sem gás bem gelada.",
        "icone": "💧",
        "acompanha_farofa": False,
    },
    {
        "id": 46,
        "nome": "Água Mineral c/ Gás",
        "categoria": "bebidas",
        "preco": 3.99,
        "destaque": False,
        "selo": "Com Gás",
        "descricao": "Garrafa de água mineral com gás bem gelada.",
        "icone": "🫧",
        "acompanha_farofa": False,
    },
    {
        "id": 47,
        "nome": "H2OH! Limoneto",
        "categoria": "bebidas",
        "preco": 7.99,
        "destaque": False,
        "selo": "Refrescante",
        "descricao": "H2OH! sabor Limoneto bem gelada.",
        "icone": "🍋",
        "acompanha_farofa": False,
    },
    {
        "id": 48,
        "nome": "Energético Monster",
        "categoria": "bebidas",
        "preco": 14.99,
        "destaque": False,
        "selo": "Lata Gelada",
        "descricao": "Energético Monster lata bem gelado.",
        "icone": "⚡",
        "acompanha_farofa": False,
    },
    {
        "id": 49,
        "nome": "Coca-Cola Lata",
        "categoria": "bebidas",
        "preco": 5.99,
        "destaque": False,
        "selo": "350ml",
        "descricao": "Refrigerante Coca-Cola em lata trincando de gelada.",
        "icone": "🥤",
        "acompanha_farofa": False,
    },
    {
        "id": 50,
        "nome": "Guaraná Lata",
        "categoria": "bebidas",
        "preco": 5.99,
        "destaque": False,
        "selo": "350ml",
        "descricao": "Refrigerante Guaraná em lata bem gelado.",
        "icone": "🥤",
        "acompanha_farofa": False,
    },
    {
        "id": 51,
        "nome": "Sprite Lata",
        "categoria": "bebidas",
        "preco": 5.99,
        "destaque": False,
        "selo": "350ml",
        "descricao": "Refrigerante Sprite em lata bem gelado.",
        "icone": "🥤",
        "acompanha_farofa": False,
    },
    {
        "id": 52,
        "nome": "Fanta Laranja / Uva",
        "categoria": "bebidas",
        "preco": 5.99,
        "destaque": False,
        "selo": "Lata 350ml",
        "descricao": "Refrigerante Fanta em lata bem gelado. Escolha entre Laranja ou Uva.",
        "icone": "🍊",
        "acompanha_farofa": False,
        "opcoes_label": "Escolha o sabor da Fanta:",
        "opcoes": [
            {"valor": "Sabor: Fanta Laranja", "label": "🍊 Fanta Laranja", "preco": 5.99},
            {"valor": "Sabor: Fanta Uva", "label": "🍇 Fanta Uva", "preco": 5.99},
        ],
    },
    {
        "id": 53,
        "nome": "Coca-Cola 1L",
        "categoria": "bebidas",
        "preco": 9.99,
        "destaque": True,
        "selo": "Para Compartilhar",
        "descricao": "Garrafa de Coca-Cola 1 Litro bem gelada.",
        "icone": "🍾",
        "acompanha_farofa": False,
    },
    {
        "id": 54,
        "nome": "Guaraná 1L",
        "categoria": "bebidas",
        "preco": 8.99,
        "destaque": True,
        "selo": "Para Compartilhar",
        "descricao": "Garrafa de Guaraná 1 Litro bem gelada.",
        "icone": "🍾",
        "acompanha_farofa": False,
    },
]


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                cliente_nome TEXT NOT NULL,
                cliente_telefone TEXT NOT NULL,
                modalidade TEXT NOT NULL,
                endereco_ou_mesa TEXT NOT NULL,
                pagamento TEXT NOT NULL,
                observacoes TEXT,
                itens_json TEXT NOT NULL,
                subtotal REAL NOT NULL,
                taxa_entrega REAL NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Na Brasa 🔥',
                criado_em TEXT NOT NULL
            )
            """
        )
        conn.commit()


init_db()


@app.route("/")
def index():
    return render_template("index.html", menu_items=MENU_ITEMS)


@app.route("/api/cardapio", methods=["GET"])
def api_cardapio():
    categoria = request.args.get("categoria", "todos")
    busca = request.args.get("q", "").strip().lower()

    itens = MENU_ITEMS
    if categoria and categoria != "todos":
        itens = [item for item in itens if item["categoria"] == categoria]

    if busca:
        itens = [
            item
            for item in itens
            if busca in item["nome"].lower() or busca in item["descricao"].lower()
        ]

    return jsonify(itens)


@app.route("/api/pedidos", methods=["GET", "POST"])
def api_pedidos():
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        cliente_nome = (dados.get("cliente_nome") or "").strip()
        cliente_telefone = (dados.get("cliente_telefone") or "").strip()
        modalidade = dados.get("modalidade") or "entrega"
        endereco_ou_mesa = (dados.get("endereco_ou_mesa") or "").strip()
        pagamento = dados.get("pagamento") or "pix"
        observacoes = (dados.get("observacoes") or "").strip()
        itens = dados.get("itens") or []

        if not cliente_nome or not itens:
            return (
                jsonify(
                    {
                        "erro": "Informe seu nome e adicione pelo menos um espetinho na comanda!"
                    }
                ),
                400,
            )

        menu_map = {item["id"]: item for item in MENU_ITEMS}
        itens_validados = []
        subtotal = 0.0

        for item_req in itens:
            item_id = int(item_req.get("id", 0))
            qtd = max(1, int(item_req.get("quantidade", 1)))
            ponto = item_req.get("ponto", "Bem Assadinho")
            if item_id in menu_map:
                produto = menu_map[item_id]
                preco_unit = float(produto["preco"])
                for op in produto.get("opcoes", []):
                    if op.get("valor") == ponto and "preco" in op:
                        preco_unit = float(op["preco"])
                        break
                total_item = round(preco_unit * qtd, 2)
                subtotal += total_item
                itens_validados.append(
                    {
                        "id": item_id,
                        "nome": produto["nome"],
                        "preco": preco_unit,
                        "quantidade": qtd,
                        "ponto": ponto,
                        "total_item": total_item,
                    }
                )

        if not itens_validados:
            return jsonify({"erro": "Nenhum item válido encontrado no pedido."}), 400

        taxa_entrega = 5.00 if modalidade == "entrega" else 0.00
        total = round(subtotal + taxa_entrega, 2)
        agora = datetime.now()
        codigo = f"CAICO-{agora.strftime('%H%M%S')}"
        criado_em = agora.strftime("%d/%m/%Y às %H:%M")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pedidos (
                    codigo, cliente_nome, cliente_telefone, modalidade,
                    endereco_ou_mesa, pagamento, observacoes, itens_json,
                    subtotal, taxa_entrega, total, status, criado_em
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    codigo,
                    cliente_nome,
                    cliente_telefone,
                    modalidade,
                    endereco_ou_mesa or "Balcão do Botequim",
                    pagamento,
                    observacoes,
                    json.dumps(itens_validados, ensure_ascii=False),
                    round(subtotal, 2),
                    taxa_entrega,
                    total,
                    "Assando na Brasa 🔥",
                    criado_em,
                ),
            )
            pedido_id = cursor.lastrowid
            conn.commit()

        return (
            jsonify(
                {
                    "sucesso": True,
                    "pedido": {
                        "id": pedido_id,
                        "codigo": codigo,
                        "cliente_nome": cliente_nome,
                        "cliente_telefone": cliente_telefone,
                        "modalidade": modalidade,
                        "endereco_ou_mesa": endereco_ou_mesa or "Balcão do Botequim",
                        "pagamento": pagamento,
                        "observacoes": observacoes,
                        "itens": itens_validados,
                        "subtotal": round(subtotal, 2),
                        "taxa_entrega": taxa_entrega,
                        "total": total,
                        "status": "Assando na Brasa 🔥",
                        "criado_em": criado_em,
                    },
                }
            ),
            201,
        )

    # GET: retorna os últimos 15 pedidos para acompanhar na Comanda Geral
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM pedidos ORDER BY id DESC LIMIT 15"
        ).fetchall()

    pedidos = []
    for row in rows:
        pedidos.append(
            {
                "id": row["id"],
                "codigo": row["codigo"],
                "cliente_nome": row["cliente_nome"],
                "modalidade": row["modalidade"],
                "endereco_ou_mesa": row["endereco_ou_mesa"],
                "pagamento": row["pagamento"],
                "observacoes": row["observacoes"],
                "itens": json.loads(row["itens_json"]),
                "subtotal": row["subtotal"],
                "taxa_entrega": row["taxa_entrega"],
                "total": row["total"],
                "status": row["status"],
                "criado_em": row["criado_em"],
            }
        )
    return jsonify(pedidos)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
