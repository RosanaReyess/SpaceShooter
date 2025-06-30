# Space Shooter - Proyecto PyGame

## Descripción del Proyecto

Space Shooter es un juego de naves espaciales desarrollado en Python utilizando la librería PyGame. El jugador controla una nave espacial que debe sobrevivir oleadas de enemigos mientras recolecta power-ups y acumula puntos.

## Características Principales

### 🎮 Funcionalidades del Juego

- **Sistema de Menús Completo**: Menú principal, pausa y game over
- **Múltiples Tipos de Enemigos**: 
  - Enemigo básico (rojo): Lento pero resistente
  - Enemigo rápido (amarillo): Veloz pero frágil  
  - Enemigo fuerte (magenta): Lento pero muy resistente
- **Sistema de Power-ups**:
  - Power-up de vida (verde): Restaura 30 puntos de vida
  - Power-up de disparo rápido (azul): Reduce el tiempo entre disparos
  - Power-up de puntos extra (amarillo): Otorga 100 puntos bonus
- **Sistema de Niveles**: La dificultad aumenta progresivamente
- **Sistema de Puntuación**: Diferentes enemigos otorgan diferentes puntos
- **Efectos Visuales**: Barras de vida, estrellas de fondo, formas geométricas variadas

### 🛠️ Funciones Personalizadas Implementadas

El proyecto incluye múltiples funciones personalizadas organizadas en clases:

#### Clase Jugador
- `mover()`: Controla el movimiento del jugador
- `disparar()`: Crea proyectiles del jugador con cooldown
- `recibir_danio()`: Maneja el sistema de vida
- `dibujar()`: Renderiza la nave del jugador con barra de vida

#### Clase Enemigo  
- `mover()`: Movimiento automático con patrones aleatorios
- `disparar()`: Sistema de disparo automático de enemigos
- `recibir_danio()`: Sistema de vida de enemigos
- `dibujar()`: Renderiza diferentes tipos de enemigos

#### Clase Bala
- `mover()`: Movimiento de proyectiles
- `esta_fuera_pantalla()`: Optimización de memoria
- `dibujar()`: Renderizado de proyectiles

#### Clase PowerUp
- `mover()`: Movimiento de power-ups
- `esta_expirado()`: Sistema de tiempo de vida
- `dibujar()`: Renderizado con símbolos distintivos

#### Clase Juego (Principal)
- `manejar_eventos()`: Sistema completo de eventos
- `actualizar_juego()`: Loop principal de lógica
- `generar_enemigos()`: Generación automática de enemigos
- `generar_powerups()`: Sistema de aparición de power-ups
- `verificar_colisiones()`: Detección de colisiones
- `aplicar_powerup()`: Efectos de los power-ups
- `dibujar_menu_principal()`: Interfaz del menú
- `dibujar_juego()`: Renderizado principal
- `dibujar_pausa()`: Pantalla de pausa
- `dibujar_game_over()`: Pantalla final
- `dibujar_hud()`: Interfaz de usuario
- `dibujar_estrellas()`: Efectos de fondo

## 🎯 Controles del Juego

- **WASD** o **Flechas**: Mover la nave
- **ESPACIO**: Disparar
- **P**: Pausar/Reanudar juego
- **Q**: Salir del juego
- **R**: Reiniciar (en game over)

## 🏆 Sistema de Puntuación

- Enemigo básico: 10 puntos
- Enemigo rápido: 15 puntos  
- Enemigo fuerte: 25 puntos
- Power-up de puntos: 100 puntos bonus

## 📋 Requisitos del Sistema

- Python 3.6 o superior
- PyGame 2.0 o superior

## 🚀 Instalación y Ejecución

1. **Instalar PyGame**:
   ```bash
   pip install pygame
   ```

2. **Ejecutar el juego**:
   ```bash
   python space_shooter.py
   ```

## 🎨 Características Técnicas

### Arquitectura del Código
- **Programación Orientada a Objetos**: Uso de clases para organizar el código
- **Separación de Responsabilidades**: Cada clase tiene una función específica
- **Funciones Personalizadas**: Más de 20 funciones custom implementadas
- **Sistema de Estados**: Manejo eficiente de diferentes pantallas del juego

### Optimizaciones Implementadas
- **Gestión de Memoria**: Eliminación automática de objetos fuera de pantalla
- **Sistema de Cooldown**: Previene spam de disparos
- **Detección de Colisiones Eficiente**: Algoritmo optimizado para múltiples objetos
- **FPS Controlado**: Mantiene 60 FPS constantes

### Elementos Visuales
- **Formas Geométricas Variadas**: Polígonos, círculos, rectángulos
- **Sistema de Colores Consistente**: Paleta de colores definida
- **Efectos Visuales**: Barras de vida, estrellas de fondo
- **Interfaz de Usuario Completa**: HUD con información relevante

## 🎮 Mecánicas de Juego

### Progresión de Dificultad
- Cada 10 enemigos eliminados se sube de nivel
- Los enemigos aparecen más frecuentemente en niveles superiores
- Variedad de tipos de enemigos con diferentes comportamientos

### Sistema de Vida y Daño
- Jugador: 100 puntos de vida máximos
- Diferentes fuentes de daño (balas enemigas, colisiones)
- Power-ups de curación disponibles

### Generación Procedural
- Aparición aleatoria de enemigos
- Tipos de enemigos seleccionados por probabilidad
- Power-ups aparecen cada 15 segundos

## 🏅 Cumplimiento de Criterios

✅ **Funciones Personalizadas**: Más de 20 funciones custom implementadas  
✅ **Múltiples Funcionalidades**: Menús, enemigos, power-ups, niveles  
✅ **Variedad de Enemigos**: 3 tipos diferentes con comportamientos únicos  
✅ **Archivo README.md**: Documentación completa del proyecto  
✅ **Uso de PyGame**: Implementación completa con PyGame (no PGZero)  

## 👩🏻‍💻 Autora

Proyecto desarrollado como trabajo práctico para demostrar el dominio de Python y PyGame, implementando conceptos avanzados de programación orientada a objetos y desarrollo de videojuegos. 
Desarrollado por: Rosana Reyes | Ingeniera de Software

---

*¡Disfruta jugando Space Shooter y demuestra tus habilidades como piloto espacial!* 🚀
  
