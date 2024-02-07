import kivy
import random
from kivy.animation import Animation
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Ellipse
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader





def colisão(rect1,rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][1]
    r1h = rect1[1][0]
    r2w = rect2[1][1]
    r2h = rect2[1][1]

    if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else:
        return False

# Tela Inicial
    
class StartMenuWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(pos=self.setter('center'))

        self.start_button = Button(
            text='Iniciar',
            size_hint=(None, None),
            size=(200, 50),
            pos=(300,200),
            on_press=self.start_game
        )
        # Imagens de Fundo e Botão
        Window.size = (800, 600)
        self.background_image = Image(source="Assets/menubg.png", size=(800,900), pos=(0,-100),)
        self.menu_text = Image(source="Assets/menutxt.png", size=(500,500), pos=(160,150))
        self.add_widget(self.background_image)
        self.add_widget(self.menu_text)
        self.add_widget(self.start_button)

        # Música
        self.menumusica = SoundLoader.load("Assets/menumusica.mp3")
        self.menumusica.loop = True
        self.menumusica.play()

    def stop_menumusica(self):
        self.menumusica.stop()

    def start_game(self, instance):
        self.parent.add_widget(JogoWidget())
        self.stop_menumusica()
        self.parent.remove_widget(self)

# Jogo

class JogoWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.recorde = 0
        self.recorde_label = Label(text=f"Recorde: {self.recorde}", font_size=32, pos=(40, 10))
        self.collision_occurred = False
        self.difficulty_counter = 0  # Add this line


        with self.canvas:
         wimg = Image(source="Assets/background.png", size=(1000,1000), pos=(-100,-200),)
         self.inimigo = AsyncImage(source="Assets/inimigo.gif", pos=(700,400),size=(100,100))
         self.add_widget(self.inimigo)
         self.jogador =  Ellipse(source="Assets/mira.png", pos=(0,0),size=(100,100))
         self.add_widget(self.recorde_label)
         self.flash = Image(source="Assets/flash.png", pos=(00,00),size=(1000,1000), color=(1,1,1,0))
    

        self.teclaPressionada = set()
        Clock.schedule_interval(self.move_step,0)

        self.musica = SoundLoader.load("Assets/ost.mp3")
        self.musica.loop = True
        self.tiro = SoundLoader.load("Assets/gunshot.wav")
        self.musica.play()

        Clock.schedule_interval(self.move_inimigo, 1.0 / 60.0)



    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        self.teclaPressionada.add(text)

    def _on_key_up(self,keyboard,keycode):
        text = keycode[1]
        if text in self.teclaPressionada:
            self.teclaPressionada.remove(text)

    def move_step(self,dt):
        xatual = self.jogador.pos[0]
        yatual = self.jogador.pos[1]

        step_size = 300 * dt
        
        max_x = Window.width - self.jogador.size[0]
        max_y = Window.height - self.jogador.size[1]

        if "w" in self.teclaPressionada and yatual < max_y:
            yatual += step_size
        if "s" in self.teclaPressionada and yatual > 0:
            yatual -= step_size
        if "a" in self.teclaPressionada and xatual > 0:
            xatual -= step_size
        if "d" in self.teclaPressionada and xatual < max_x:
            xatual += step_size

        self.jogador.pos = (xatual,yatual)

    def surgir(self, *args):
        anim = Animation(color=[1,1,1,0.2], duration = 0)
        anim.start(self.flash)

    def sumir(self, *args):
        anim = Animation(color=[1,1,1,0], duration = 0.2)
        anim.start(self.flash)

    def move_inimigo(self, dt):
        x, y = self.inimigo.pos
        x -= 300 * dt
        self.inimigo.pos = (x, y)
        if colisão((self.jogador.pos, self.jogador.size), (self.inimigo.pos, self.inimigo.size)) and not self.collision_occurred:
            print("Tocou")
            self.tiro.play()
            self.recorde += 1
            self.recorde_label.text = f"Recorde: {self.recorde}"
            self.collision_occurred = True
            self.surgir()
            Clock.schedule_once(self.sumir, 0.2)
            Clock.schedule_once(self.reset_collision, 1.5)
            self.difficulty_counter += 1

        else:
            print("Não tocou")
        if x < -100:
            x = Window.width + 100
            y = random.randint(0, Window.height - self.inimigo.size[1])
            self.inimigo.pos = (x, y)

    def reset_collision(self, dt):
        self.collision_occurred = False


class MeuApp(App):
    def build(self):
        return StartMenuWidget()
    
if __name__ == "__main__":
    app = MeuApp()
    app.run()
    
