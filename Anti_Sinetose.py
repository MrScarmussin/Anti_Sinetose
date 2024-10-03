import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor

class Overlay(QWidget):
    def __init__(self, circle_positions, circle_size, transparency):
        super().__init__()
        self.transparency = transparency
        self.circle_positions = circle_positions
        self.circle_size = circle_size
        self.dragging_circle = None  # Indica se um círculo está sendo arrastado
        self.offset = QPoint(0, 0)  # Offset entre o clique do mouse e o centro do círculo
        self.edit_mode = False  # Variável para alternar o modo de edição
        self.initUI()

    def initUI(self):
        # Configura a janela para ser sem bordas e transparente
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

    def paintEvent(self, event):
        # Método para desenhar os círculos
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        brush = QBrush(QColor(255, 0, 0, self.transparency))  # Cor e transparência do círculo
        
        for pos in self.circle_positions:
            painter.setBrush(brush)
            painter.drawEllipse(pos[0], pos[1], self.circle_size, self.circle_size)

    def mousePressEvent(self, event):
        # Se estiver no modo de edição, verificar se o usuário clicou em um círculo
        if self.edit_mode:
            for i, pos in enumerate(self.circle_positions):
                # Verifica se o clique do mouse está dentro de um círculo
                if (pos[0] <= event.x() <= pos[0] + self.circle_size and
                    pos[1] <= event.y() <= pos[1] + self.circle_size):
                    self.dragging_circle = i
                    # Calcula o offset do clique dentro do círculo
                    self.offset = QPoint(event.x() - pos[0], event.y() - pos[1])
                    break

    def mouseMoveEvent(self, event):
        # Arrasta o círculo se estiver no modo de edição
        if self.edit_mode and self.dragging_circle is not None:
            # Atualiza a posição do círculo com base no movimento do mouse
            self.circle_positions[self.dragging_circle] = (event.x() - self.offset.x(), event.y() - self.offset.y())
            self.update()  # Redesenha os círculos com as novas posições

    def mouseReleaseEvent(self, event):
        # Libera o círculo após soltar o botão do mouse
        if self.edit_mode:
            self.dragging_circle = None

    def toggle_edit_mode(self):
        # Alterna o modo de edição
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            print("Modo de edição ativado. Arraste os círculos para movê-los.")
        else:
            print("Modo de edição desativado.")
    
    # Função para alterar o tamanho dos círculos
    def change_circle_size(self, new_size):
        self.circle_size = new_size  # Atualiza o tamanho dos círculos
        self.update()  # Redesenha os círculos com o novo tamanho

    def change_transparency(self, new_transparency):
        self.transparency = new_transparency
        self.update()
        

# Função que ficará em loop até o usuário digitar "sair" ou "editar"
def check_terminal_commands(app, overlay):
    while True:
        command = input(
            """Digite:
'1' para fechar o programa 
'2' para mover os círculos 
'3' para alterar o tamanho dos circulos. 
'4' para alterar a transparencia dos circulos.
>>> """).strip().lower()
        if command == '1':
            print("Encerrando o programa...")
            app.quit()  # Fecha a aplicação PyQt
            break
        elif command == '2':
            overlay.toggle_edit_mode()  # Alterna o modo de edição
        elif command == '3':
            change_circle_size(overlay) # altera o tamanho dos circulos
        elif command == '4':
            change_transparency(overlay) # Alterna a transparencia

def change_circle_size(overlay):
    print('Digite um tamanho para os círculos. \n Padrão: Pequeno (15), Grande (30)')
    new_size = int(input('>>> '))
    overlay.change_circle_size(new_size)

def change_transparency(overlay):
    print('Digite um valor de transparencia para os círculos (0 - 100) \n Padrão: 100')
    new_transparency = int(int(input('>>> ')) * 255 / 100)
    
    overlay.change_transparency(new_transparency)
    


if __name__ == '__main__':
    os.system('cls')
    print('Bem vinda ao ANTI-CINETOSE! \n')
    
    print('Digite quantos círculos você deseja: \n PARA RED DEAD REDEMPTION OU GTA, USE 4 DEVIDO AO MINI MAPA')
    num_of_circles = int(input('>>> '))
    
    print(f'Certo, qual o tamanho deles? \nUse [G] para grande (30x30) \nUse [P] para pequeno (15x15) \n')
    circle_size_input = input('>>> ').lower()

    # Define o tamanho dos círculos com base na escolha
    transparency = 255
    big_circle = 30
    small_circle = 15
    if circle_size_input == 'g':
        circle_size = big_circle
    else:
        circle_size = small_circle

    # Gera posições de círculo 
    screen_width, screen_height = 1920, 1200  
    circle_positions = [(screen_width//2, screen_height//2)]  # Adiciona o primeiro círculo ao centro

    ## ADICIONAR FUNÇÃO PARA EDITAR DURANTE EXECUÇÃO ##
    recuo = 200 #editar conforme a vontade, 


    base_circles_positions = [(screen_width - recuo, screen_height - recuo),  
                              (screen_width - recuo, recuo),
                              (recuo, recuo),
                              (recuo , screen_height - recuo),]
    # Adiciona mais círculos espalhados pela tela
    if (num_of_circles > 1):
        for i in range(num_of_circles-1):
            circle_positions.append(base_circles_positions[i])  

    # Inicializa o PyQt
    app = QApplication(sys.argv)
    overlay = Overlay(circle_positions, circle_size, transparency)
    overlay.show()

    # Cria uma thread para ouvir os comandos 'sair' e 'editar'
    terminal_thread = threading.Thread(target=check_terminal_commands, args=(app, overlay))
    terminal_thread.start()

    # Executa a interface PyQt
    sys.exit(app.exec_())

