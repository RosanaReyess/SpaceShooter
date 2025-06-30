import pygame
import random
import sys
import math

# Inicializar pygame
pygame.init()

# Constantes del juego
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Estados del juego
MENU_PRINCIPAL = 0
JUGANDO = 1
GAME_OVER = 2
PAUSA = 3

class Jugador:
    """Clase que representa al jugador"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 40
        self.velocidad = 5
        self.vida = 100
        self.vida_maxima = 100
        self.puntuacion = 0
        self.ultimo_disparo = 0
        self.cooldown_disparo = 250  # milisegundos
        
    def mover(self, teclas):
        """Función para mover al jugador según las teclas presionadas"""
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidad
            
        # Mantener al jugador dentro de la pantalla
        self.x = max(0, min(self.x, ANCHO_PANTALLA - self.ancho))
        self.y = max(0, min(self.y, ALTO_PANTALLA - self.alto))
    
    def disparar(self):
        """Función para crear un disparo del jugador"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > self.cooldown_disparo:
            self.ultimo_disparo = tiempo_actual
            return Bala(self.x + self.ancho // 2, self.y, -8, CYAN)
        return None
    
    def recibir_danio(self, danio):
        """Función para recibir daño"""
        self.vida -= danio
        if self.vida < 0:
            self.vida = 0
    
    def dibujar(self, pantalla):
        """Función para dibujar al jugador"""
        # Cuerpo principal de la nave
        pygame.draw.polygon(pantalla, VERDE, [
            (self.x + self.ancho // 2, self.y),
            (self.x, self.y + self.alto),
            (self.x + self.ancho // 4, self.y + self.alto - 10),
            (self.x + self.ancho - self.ancho // 4, self.y + self.alto - 10),
            (self.x + self.ancho, self.y + self.alto)
        ])
        
        # Barra de vida
        barra_ancho = 60
        barra_alto = 8
        porcentaje_vida = self.vida / self.vida_maxima
        
        # Fondo de la barra de vida
        pygame.draw.rect(pantalla, ROJO, 
                        (self.x - 5, self.y - 15, barra_ancho, barra_alto))
        # Vida actual
        pygame.draw.rect(pantalla, VERDE, 
                        (self.x - 5, self.y - 15, barra_ancho * porcentaje_vida, barra_alto))

class Enemigo:
    """Clase que representa a los enemigos"""
    def __init__(self, x, y, tipo=1):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = random.randint(1, 3)
        self.ultimo_disparo = 0
        self.cooldown_disparo = random.randint(1000, 3000)
        
        # Propiedades según el tipo de enemigo
        if tipo == 1:  # Enemigo básico
            self.ancho = 30
            self.alto = 30
            self.vida = 20
            self.puntos = 10
            self.color = ROJO
        elif tipo == 2:  # Enemigo rápido
            self.ancho = 25
            self.alto = 25
            self.vida = 15
            self.puntos = 15
            self.velocidad += 2
            self.color = AMARILLO
        else:  # Enemigo fuerte
            self.ancho = 40
            self.alto = 35
            self.vida = 40
            self.puntos = 25
            self.velocidad -= 1
            self.color = MAGENTA
    
    def mover(self):
        """Función para mover al enemigo"""
        self.y += self.velocidad
        # Movimiento lateral aleatorio
        if random.randint(1, 100) < 5:
            self.x += random.randint(-20, 20)
            self.x = max(0, min(self.x, ANCHO_PANTALLA - self.ancho))
    
    def disparar(self):
        """Función para que el enemigo dispare"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > self.cooldown_disparo:
            self.ultimo_disparo = tiempo_actual
            self.cooldown_disparo = random.randint(1000, 3000)
            return Bala(self.x + self.ancho // 2, self.y + self.alto, 4, self.color)
        return None
    
    def recibir_danio(self, danio):
        """Función para recibir daño"""
        self.vida -= danio
        return self.vida <= 0
    
    def dibujar(self, pantalla):
        """Función para dibujar al enemigo"""
        if self.tipo == 1:
            # Enemigo básico - rectángulo
            pygame.draw.rect(pantalla, self.color, 
                           (self.x, self.y, self.ancho, self.alto))
        elif self.tipo == 2:
            # Enemigo rápido - triángulo
            pygame.draw.polygon(pantalla, self.color, [
                (self.x + self.ancho // 2, self.y + self.alto),
                (self.x, self.y),
                (self.x + self.ancho, self.y)
            ])
        else:
            # Enemigo fuerte - hexágono
            centro_x = self.x + self.ancho // 2
            centro_y = self.y + self.alto // 2
            puntos = []
            for i in range(6):
                angulo = i * 60 * math.pi / 180
                px = centro_x + self.ancho // 2 * math.cos(angulo)
                py = centro_y + self.alto // 2 * math.sin(angulo)
                puntos.append((px, py))
            pygame.draw.polygon(pantalla, self.color, puntos)

class Bala:
    """Clase que representa las balas"""
    def __init__(self, x, y, velocidad, color):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.color = color
        self.ancho = 4
        self.alto = 10
        self.danio = 10
    
    def mover(self):
        """Función para mover la bala"""
        self.y += self.velocidad
    
    def esta_fuera_pantalla(self):
        """Función para verificar si la bala salió de la pantalla"""
        return self.y < 0 or self.y > ALTO_PANTALLA
    
    def dibujar(self, pantalla):
        """Función para dibujar la bala"""
        pygame.draw.rect(pantalla, self.color, 
                        (self.x - self.ancho // 2, self.y, self.ancho, self.alto))

class PowerUp:
    """Clase que representa los power-ups"""
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo  # 1: vida, 2: disparo rápido, 3: puntos extra
        self.velocidad = 2
        self.ancho = 20
        self.alto = 20
        self.tiempo_vida = 10000  # 10 segundos
        self.creado = pygame.time.get_ticks()
        
        # Colores según el tipo
        if tipo == 1:
            self.color = VERDE
        elif tipo == 2:
            self.color = AZUL
        else:
            self.color = AMARILLO
    
    def mover(self):
        """Función para mover el power-up"""
        self.y += self.velocidad
    
    def esta_expirado(self):
        """Función para verificar si el power-up expiró"""
        return pygame.time.get_ticks() - self.creado > self.tiempo_vida
    
    def dibujar(self, pantalla):
        """Función para dibujar el power-up"""
        pygame.draw.circle(pantalla, self.color, 
                          (self.x + self.ancho // 2, self.y + self.alto // 2), 
                          self.ancho // 2)
        # Símbolo según el tipo
        if self.tipo == 1:  # Vida
            pygame.draw.line(pantalla, BLANCO, 
                           (self.x + 5, self.y + 10), (self.x + 15, self.y + 10), 2)
            pygame.draw.line(pantalla, BLANCO, 
                           (self.x + 10, self.y + 5), (self.x + 10, self.y + 15), 2)

class Juego:
    """Clase principal del juego"""
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Space Shooter - Proyecto PyGame")
        self.reloj = pygame.time.Clock()
        self.estado = MENU_PRINCIPAL
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Inicializar objetos del juego
        self.reiniciar_juego()
        
        # Variables para generar enemigos
        self.ultimo_enemigo = 0
        self.intervalo_enemigos = 2000  # 2 segundos
        
        # Variables para power-ups
        self.ultimo_powerup = 0
        self.intervalo_powerups = 15000  # 15 segundos
    
    def reiniciar_juego(self):
        """Función para reiniciar el juego"""
        self.jugador = Jugador(ANCHO_PANTALLA // 2 - 25, ALTO_PANTALLA - 60)
        self.balas_jugador = []
        self.balas_enemigos = []
        self.enemigos = []
        self.powerups = []
        self.nivel = 1
        self.enemigos_eliminados = 0
    
    def manejar_eventos(self):
        """Función para manejar los eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if self.estado == MENU_PRINCIPAL:
                    if evento.key == pygame.K_SPACE:
                        self.estado = JUGANDO
                        self.reiniciar_juego()
                    elif evento.key == pygame.K_q:
                        return False
                
                elif self.estado == JUGANDO:
                    if evento.key == pygame.K_SPACE:
                        bala = self.jugador.disparar()
                        if bala:
                            self.balas_jugador.append(bala)
                    elif evento.key == pygame.K_p:
                        self.estado = PAUSA
                
                elif self.estado == PAUSA:
                    if evento.key == pygame.K_p:
                        self.estado = JUGANDO
                
                elif self.estado == GAME_OVER:
                    if evento.key == pygame.K_r:
                        self.estado = MENU_PRINCIPAL
                    elif evento.key == pygame.K_q:
                        return False
        
        return True
    
    def actualizar_juego(self):
        """Función principal para actualizar la lógica del juego"""
        if self.estado != JUGANDO:
            return
        
        # Mover jugador
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas)
        
        # Generar enemigos
        self.generar_enemigos()
        
        # Generar power-ups
        self.generar_powerups()
        
        # Actualizar balas del jugador
        self.actualizar_balas_jugador()
        
        # Actualizar balas de enemigos
        self.actualizar_balas_enemigos()
        
        # Actualizar enemigos
        self.actualizar_enemigos()
        
        # Actualizar power-ups
        self.actualizar_powerups()
        
        # Verificar colisiones
        self.verificar_colisiones()
        
        # Verificar game over
        if self.jugador.vida <= 0:
            self.estado = GAME_OVER
        
        # Verificar subida de nivel
        if self.enemigos_eliminados >= self.nivel * 10:
            self.nivel += 1
            self.intervalo_enemigos = max(500, self.intervalo_enemigos - 200)
    
    def generar_enemigos(self):
        """Función para generar enemigos automáticamente"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_enemigo > self.intervalo_enemigos:
            self.ultimo_enemigo = tiempo_actual
            x = random.randint(0, ANCHO_PANTALLA - 40)
            tipo = random.choices([1, 2, 3], weights=[60, 25, 15])[0]
            self.enemigos.append(Enemigo(x, -40, tipo))
    
    def generar_powerups(self):
        """Función para generar power-ups"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_powerup > self.intervalo_powerups:
            self.ultimo_powerup = tiempo_actual
            x = random.randint(0, ANCHO_PANTALLA - 20)
            tipo = random.randint(1, 3)
            self.powerups.append(PowerUp(x, -20, tipo))
    
    def actualizar_balas_jugador(self):
        """Función para actualizar las balas del jugador"""
        for bala in self.balas_jugador[:]:
            bala.mover()
            if bala.esta_fuera_pantalla():
                self.balas_jugador.remove(bala)
    
    def actualizar_balas_enemigos(self):
        """Función para actualizar las balas de los enemigos"""
        for bala in self.balas_enemigos[:]:
            bala.mover()
            if bala.esta_fuera_pantalla():
                self.balas_enemigos.remove(bala)
    
    def actualizar_enemigos(self):
        """Función para actualizar los enemigos"""
        for enemigo in self.enemigos[:]:
            enemigo.mover()
            
            # Enemigo dispara
            bala = enemigo.disparar()
            if bala:
                self.balas_enemigos.append(bala)
            
            # Eliminar enemigos que salieron de la pantalla
            if enemigo.y > ALTO_PANTALLA:
                self.enemigos.remove(enemigo)
    
    def actualizar_powerups(self):
        """Función para actualizar los power-ups"""
        for powerup in self.powerups[:]:
            powerup.mover()
            if powerup.y > ALTO_PANTALLA or powerup.esta_expirado():
                self.powerups.remove(powerup)
    
    def verificar_colisiones(self):
        """Función para verificar todas las colisiones"""
        # Colisiones balas jugador vs enemigos
        for bala in self.balas_jugador[:]:
            for enemigo in self.enemigos[:]:
                if self.hay_colision(bala, enemigo):
                    self.balas_jugador.remove(bala)
                    if enemigo.recibir_danio(bala.danio):
                        self.enemigos.remove(enemigo)
                        self.jugador.puntuacion += enemigo.puntos
                        self.enemigos_eliminados += 1
                    break
        
        # Colisiones balas enemigos vs jugador
        for bala in self.balas_enemigos[:]:
            if self.hay_colision(bala, self.jugador):
                self.balas_enemigos.remove(bala)
                self.jugador.recibir_danio(bala.danio)
        
        # Colisiones enemigos vs jugador
        for enemigo in self.enemigos[:]:
            if self.hay_colision(enemigo, self.jugador):
                self.enemigos.remove(enemigo)
                self.jugador.recibir_danio(20)
        
        # Colisiones power-ups vs jugador
        for powerup in self.powerups[:]:
            if self.hay_colision(powerup, self.jugador):
                self.powerups.remove(powerup)
                self.aplicar_powerup(powerup)
    
    def hay_colision(self, obj1, obj2):
        """Función para detectar colisión entre dos objetos"""
        return (obj1.x < obj2.x + obj2.ancho and
                obj1.x + obj1.ancho > obj2.x and
                obj1.y < obj2.y + obj2.alto and
                obj1.y + obj1.alto > obj2.y)
    
    def aplicar_powerup(self, powerup):
        """Función para aplicar el efecto del power-up"""
        if powerup.tipo == 1:  # Vida
            self.jugador.vida = min(self.jugador.vida_maxima, self.jugador.vida + 30)
        elif powerup.tipo == 2:  # Disparo rápido
            self.jugador.cooldown_disparo = max(100, self.jugador.cooldown_disparo - 50)
        else:  # Puntos extra
            self.jugador.puntuacion += 100
    
    def dibujar_menu_principal(self):
        """Función para dibujar el menú principal"""
        self.pantalla.fill(NEGRO)
        
        # Título
        titulo = self.fuente.render("SPACE SHOOTER", True, BLANCO)
        rect_titulo = titulo.get_rect(center=(ANCHO_PANTALLA // 2, 150))
        self.pantalla.blit(titulo, rect_titulo)
        
        # Instrucciones
        instrucciones = [
            "WASD o Flechas: Mover",
            "ESPACIO: Disparar",
            "P: Pausa",
            "",
            "Presiona ESPACIO para jugar",
            "Q para salir"
        ]
        
        y = 250
        for linea in instrucciones:
            if linea:
                texto = self.fuente_pequena.render(linea, True, BLANCO)
                rect_texto = texto.get_rect(center=(ANCHO_PANTALLA // 2, y))
                self.pantalla.blit(texto, rect_texto)
            y += 30
    
    def dibujar_juego(self):
        """Función para dibujar el juego"""
        self.pantalla.fill(NEGRO)
        
        # Dibujar estrellas de fondo
        self.dibujar_estrellas()
        
        # Dibujar jugador
        self.jugador.dibujar(self.pantalla)
        
        # Dibujar balas
        for bala in self.balas_jugador:
            bala.dibujar(self.pantalla)
        for bala in self.balas_enemigos:
            bala.dibujar(self.pantalla)
        
        # Dibujar enemigos
        for enemigo in self.enemigos:
            enemigo.dibujar(self.pantalla)
        
        # Dibujar power-ups
        for powerup in self.powerups:
            powerup.dibujar(self.pantalla)
        
        # Dibujar HUD
        self.dibujar_hud()
    
    def dibujar_estrellas(self):
        """Función para dibujar estrellas de fondo"""
        for _ in range(50):
            x = random.randint(0, ANCHO_PANTALLA)
            y = random.randint(0, ALTO_PANTALLA)
            pygame.draw.circle(self.pantalla, BLANCO, (x, y), 1)
    
    def dibujar_hud(self):
        """Función para dibujar la interfaz de usuario"""
        # Puntuación
        texto_puntos = self.fuente_pequena.render(f"Puntos: {self.jugador.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto_puntos, (10, 10))
        
        # Nivel
        texto_nivel = self.fuente_pequena.render(f"Nivel: {self.nivel}", True, BLANCO)
        self.pantalla.blit(texto_nivel, (10, 35))
        
        # Vida
        texto_vida = self.fuente_pequena.render(f"Vida: {self.jugador.vida}/{self.jugador.vida_maxima}", True, BLANCO)
        self.pantalla.blit(texto_vida, (10, 60))
        
        # Enemigos eliminados
        texto_enemigos = self.fuente_pequena.render(f"Enemigos: {self.enemigos_eliminados}", True, BLANCO)
        self.pantalla.blit(texto_enemigos, (ANCHO_PANTALLA - 150, 10))
    
    def dibujar_pausa(self):
        """Función para dibujar la pantalla de pausa"""
        # Dibujar el juego de fondo con transparencia
        self.dibujar_juego()
        
        # Overlay semi-transparente
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        overlay.set_alpha(128)
        overlay.fill(NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        
        # Texto de pausa
        texto_pausa = self.fuente.render("PAUSA", True, BLANCO)
        rect_pausa = texto_pausa.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
        self.pantalla.blit(texto_pausa, rect_pausa)
        
        texto_continuar = self.fuente_pequena.render("Presiona P para continuar", True, BLANCO)
        rect_continuar = texto_continuar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 50))
        self.pantalla.blit(texto_continuar, rect_continuar)
    
    def dibujar_game_over(self):
        """Función para dibujar la pantalla de game over"""
        self.pantalla.fill(NEGRO)
        
        # Game Over
        texto_game_over = self.fuente.render("GAME OVER", True, ROJO)
        rect_game_over = texto_game_over.get_rect(center=(ANCHO_PANTALLA // 2, 200))
        self.pantalla.blit(texto_game_over, rect_game_over)
        
        # Estadísticas finales
        estadisticas = [
            f"Puntuación Final: {self.jugador.puntuacion}",
            f"Nivel Alcanzado: {self.nivel}",
            f"Enemigos Eliminados: {self.enemigos_eliminados}",
            "",
            "R: Volver al menú",
            "Q: Salir"
        ]
        
        y = 300
        for linea in estadisticas:
            if linea:
                texto = self.fuente_pequena.render(linea, True, BLANCO)
                rect_texto = texto.get_rect(center=(ANCHO_PANTALLA // 2, y))
                self.pantalla.blit(texto, rect_texto)
            y += 30
    
    def ejecutar(self):
        """Función principal para ejecutar el juego"""
        ejecutando = True
        
        while ejecutando:
            # Manejar eventos
            ejecutando = self.manejar_eventos()
            
            # Actualizar juego
            self.actualizar_juego()
            
            # Dibujar según el estado
            if self.estado == MENU_PRINCIPAL:
                self.dibujar_menu_principal()
            elif self.estado == JUGANDO:
                self.dibujar_juego()
            elif self.estado == PAUSA:
                self.dibujar_pausa()
            elif self.estado == GAME_OVER:
                self.dibujar_game_over()
            
            # Actualizar pantalla
            pygame.display.flip()
            self.reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Función principal
def main():
    """Función principal del programa"""
    print("Iniciando Space Shooter...")
    print("Controles:")
    print("- WASD o Flechas: Mover")
    print("- ESPACIO: Disparar")
    print("- P: Pausa")
    print("- Q: Salir")
    
    juego = Juego()
    juego.ejecutar()

# Ejecutar el juego si este archivo es ejecutado directamente
if __name__ == "__main__":
    main()