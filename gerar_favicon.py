#!/usr/bin/env python3
"""
Script para gerar favicon do ZERO 1
Cria um favicon verde com o número 1 no centro
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Criar diretório static se não existir
    os.makedirs('static', exist_ok=True)

    # Tamanhos de favicon
    sizes = [16, 32, 48, 64, 128, 256]

    for size in sizes:
        # Criar imagem
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Desenhar círculo verde
        margin = 2
        draw.ellipse(
            [(margin, margin), (size - margin, size - margin)],
            fill='#4caf50',
            outline='#2e7d32',
            width=max(1, size // 32)
        )
        
        # Desenhar círculo interno (glow)
        glow_margin = margin + max(2, size // 16)
        draw.ellipse(
            [(glow_margin, glow_margin), (size - glow_margin, size - glow_margin)],
            outline='#66bb6a',
            width=max(1, size // 48)
        )
        
        # Desenhar número 1
        try:
            # Tentar usar fonte do sistema
            font_size = int(size * 0.6)
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        except:
            try:
                font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', font_size)
            except:
                # Fallback para fonte padrão
                font = ImageFont.load_default()
        
        text = "1"
        
        # Centralizar texto
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2 - bbox[0]
        y = (size - text_height) // 2 - bbox[1]
        
        # Sombra
        shadow_offset = max(1, size // 32)
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 80))
        
        # Texto principal
        draw.text((x, y), text, font=font, fill='white')
        
        # Salvar
        if size == 16:
            img.save('static/favicon.ico', format='ICO', sizes=[(16, 16)])
        img.save(f'static/favicon-{size}x{size}.png')
        print(f"✅ Criado favicon-{size}x{size}.png")

    # Criar também apple-touch-icon
    img_180 = Image.new('RGBA', (180, 180), (0, 0, 0, 0))
    draw_180 = ImageDraw.Draw(img_180)
    
    # Círculo verde
    margin_180 = 4
    draw_180.ellipse(
        [(margin_180, margin_180), (180 - margin_180, 180 - margin_180)],
        fill='#4caf50',
        outline='#2e7d32',
        width=6
    )
    
    # Círculo interno
    glow_margin_180 = margin_180 + 8
    draw_180.ellipse(
        [(glow_margin_180, glow_margin_180), (180 - glow_margin_180, 180 - glow_margin_180)],
        outline='#66bb6a',
        width=4
    )
    
    # Número 1
    try:
        font_180 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 108)
    except:
        try:
            font_180 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 108)
        except:
            font_180 = ImageFont.load_default()
    
    bbox_180 = draw_180.textbbox((0, 0), "1", font=font_180)
    text_width_180 = bbox_180[2] - bbox_180[0]
    text_height_180 = bbox_180[3] - bbox_180[1]
    
    x_180 = (180 - text_width_180) // 2 - bbox_180[0]
    y_180 = (180 - text_height_180) // 2 - bbox_180[1]
    
    # Sombra
    draw_180.text((x_180 + 4, y_180 + 4), "1", font=font_180, fill=(0, 0, 0, 80))
    
    # Texto
    draw_180.text((x_180, y_180), "1", font=font_180, fill='white')
    
    img_180.save('static/apple-touch-icon.png')
    print("✅ Criado apple-touch-icon.png")
    
    print("\n🎉 Favicons criados com sucesso!")
    print("\nArquivos gerados:")
    print("  - static/favicon.ico (16x16)")
    print("  - static/favicon.svg")
    for size in sizes:
        print(f"  - static/favicon-{size}x{size}.png")
    print("  - static/apple-touch-icon.png (180x180)")

except ImportError:
    print("⚠️  Pillow não instalado. Instalando...")
    import subprocess
    subprocess.run(['pip', 'install', 'Pillow'])
    print("✅ Pillow instalado! Execute o script novamente:")
    print("   python gerar_favicon.py")
except Exception as e:
    print(f"❌ Erro: {e}")
    print("\nUsando apenas SVG (já criado).")
