import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_avaliacoes():
    url = entrada_url.get()
    if not url:
        messagebox.showwarning("Atenção", "Por favor, insira uma URL.")
        return

    try:
        # Configurar o ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Roda sem abrir a janela do Chrome
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        # Espera explícita para garantir que o conteúdo seja carregado
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-details .text")))

        # Rolar a página para garantir que o conteúdo dinâmico seja carregado
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Aguardar o carregamento

        # Coletar avaliações usando o seletor correto para a classe 'text'
        avaliacoes = driver.find_elements(By.CSS_SELECTOR, ".review-details .text")  # Seletor de avaliação

        saida_texto.delete(1.0, tk.END)

        if not avaliacoes:
            saida_texto.insert(tk.END, "Nenhuma avaliação encontrada.")
            driver.quit()
            return

        for avaliacao in avaliacoes:
            texto = avaliacao.text.strip()
            if texto:
                saida_texto.insert(tk.END, f"{texto}\n{'-'*40}\n")

        driver.quit()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar avaliações:\n{e}")

# Criar a janela
janela = tk.Tk()
janela.title("Raspador de Avaliações - Americanas")

tk.Label(janela, text="URL do Produto:").pack(pady=5)
entrada_url = tk.Entry(janela, width=80)
entrada_url.pack(pady=5)

botao_buscar = tk.Button(janela, text="Buscar Avaliações", command=buscar_avaliacoes)
botao_buscar.pack(pady=10)

saida_texto = tk.Text(janela, width=100, height=20)
saida_texto.pack(pady=5)

janela.mainloop()