import pygame
import random

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
FPS = 60
MAX_COUNT_OF_ENEMIES = 5
ENEMY_EVENT_TYPE = 30


# класс главного героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        # координаты главного героя
        self.x, self.y = position

        # здоровье главного героя
        self.health = 100

        # количество пуль от игрока на экране
        self.bullets_count = 0

        # наносимый урон
        self.damage = 1

        # радиус главного героя
        self.radius = 25

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        self.image = pygame.image.load('img/ship1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 70))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return (self.image, self.rect)


# класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, damage):
        pygame.sprite.Sprite.__init__(self)

        # координаты пули
        self.x, self.y = position

        # направление пули (вверх или вниз)
        self.direction = direction

        # наносимый урон
        self.damage = damage

        # радиус пули
        self.radius = 5

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        if self.direction == -1:
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), self.radius)


# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # координаты врага
        self.x, self.y = position
        # направление по оси x(увеличение или уменьшение)
        self.direction = random.choice([-1, 1])

        # счетчик для выстрела
        self.kd_counter = 0

        # продолжительность перезарядки
        self.reload = random.randint(15, 45)

        # здоровье врага
        self.hp = 1

        # наносимый урон
        self.damage = 1

        # радиус врага
        self.radius = 12

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)


# класс астероида
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # координаты астероида
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = 0

        # изменение координат за один цикл
        self.dx = random.randint(-10, 10)
        self.dy = random.randint(1, 10)

        # здоровье астероида
        self.hp = random.randint(1, 4)

        # радиус астероида
        self.radius = (self.hp + 2) * 5

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (110, 110, 110), (self.x, self.y), self.radius)


# класс пули
class Buff(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)

        # координаты баффа
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = 0

        # радиус баффа
        self.radius = 15

        # скорость баффа
        self.speed = random.randint(5, 10)

        # тип баффа
        self.type = type

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        if self.type == 0:
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(screen, (0, 255, 255), (self.x, self.y), self.radius)


# класс игры
class Game:
    def __init__(self, hero):
        # все динамичные объекты
        self.hero = hero
        self.bullets = []
        self.enemies = []
        self.asteroids = []
        self.buffs = []

    # отрисовка всех динамичных объектов
    def render(self, screen):
        # отрисовка главного героя
        self.hero.render(screen)

        # отрисовка всех врагов
        for enemy in self.enemies:
            enemy.render(screen)

        # отрисовка всех астероидов
        for asteroid in self.asteroids:
            asteroid.render(screen)

        # отрисовка всех пуль
        for bullet in self.bullets:
            bullet.render(screen)

        # отрисовка всех баффов
        for buff in self.buffs:
            buff.render(screen)

    # движение главного героя
    def move_hero(self):
        # импорт текущих координат из класса hero
        next_x, next_y = self.hero.get_position()
        if next_x < 0:
            next_x = WINDOW_WIDTH
        if next_x > WINDOW_WIDTH:
            next_x = 0
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 10
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += 10
        if pygame.key.get_pressed()[pygame.K_w] and self.hero.get_position()[1] > 10:
            next_y -= 10
        if pygame.key.get_pressed()[pygame.K_s] and self.hero.get_position()[1] < WINDOW_HEIGHT - 10:
            next_y += 10
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed() == (1, 0, 0):
            if self.hero.bullets_count < 20:
                self.bullets.append(Bullet((next_x, next_y), -1, self.hero.damage))
                self.hero.bullets_count += 1
        # изменить координаты
        self.hero.set_position((next_x, next_y))

    # движение пули
    def move_bullets(self):
        # проход по всем действующим пулям
        for i, bullet in enumerate(self.bullets):
            bullet.set_position((bullet.get_position()[0], bullet.get_position()[1] + bullet.direction * 4))
            # выход пули за пределы экрана
            if bullet.get_position()[1] < 0 or bullet.get_position()[1] > WINDOW_HEIGHT:
                if bullet.direction == -1:
                    # уменьшение счетчика пуль главного героя
                    self.hero.bullets_count -= 1
                del self.bullets[i]
            # свои пули
            if bullet.direction == -1:
                # стрельба по врагам
                for j, enemy in enumerate(self.enemies):
                    if abs(enemy.get_position()[0] - bullet.get_position()[0]) < enemy.radius + bullet.radius and abs(
                            enemy.get_position()[1] - bullet.get_position()[1]) < enemy.radius + bullet.radius:
                        # уничтожение пули и нанесение урона врагу
                        del self.bullets[i]
                        enemy.hp -= self.hero.damage

                        # уничтожение астероида
                        if enemy.hp == 0:
                            del self.enemies[j]
                        # увеличение счетчика пуль главного героя
                        self.hero.bullets_count -= 1
                # стрельба по астероидам
                for j, asteroid in enumerate(self.asteroids):
                    if abs(asteroid.get_position()[0] - bullet.get_position()[
                        0]) < asteroid.radius + bullet.radius and abs(
                            asteroid.get_position()[1] - bullet.get_position()[1]) < asteroid.radius + bullet.radius:
                        # уничтожение пули и нанесение урона астероиду
                        del self.bullets[i]
                        asteroid.hp -= self.hero.damage

                        # уничтожение астероида
                        if asteroid.hp == 0:
                            del self.asteroids[j]
                        # увеличение счетчика пуль главного героя
                        self.hero.bullets_count -= 1
            # вражеские пули
            else:
                if abs(self.hero.get_position()[0] - bullet.get_position()[
                    0]) < self.hero.radius + bullet.radius and abs(
                        self.hero.get_position()[1] - bullet.get_position()[1]) < self.hero.radius + bullet.radius:
                    # уничтожение пули
                    self.hero.health -= bullet.damage

                    # снятие здоровья у героя
                    if self.hero.health < 0:
                        self.hero.health = 0
                    del self.bullets[i]

                    # вывод показателя здоровья главного героя в консоль
                    print(f"HEALTH: {self.hero.health}")

    # движение врагов
    def move_enemies(self):
        # просмотр каждого врага по отдельности
        for i, enemy in enumerate(self.enemies):
            # движение от одной части экрана к другой
            if enemy.get_position()[0] > WINDOW_WIDTH:
                enemy.direction = -1
            elif enemy.get_position()[0] < 0:
                enemy.direction = 1
            # увеличение счетчика стрельбы врага
            enemy.kd_counter += 1
            # выстрел врага
            if enemy.kd_counter == enemy.reload:
                self.bullets.append(Bullet(enemy.get_position(), 1, enemy.damage))
                enemy.kd_counter = 0
            # движение врага
            enemy.set_position((enemy.get_position()[0] + enemy.direction * 3, enemy.get_position()[1]))

    # движение астероидов
    def move_asteroids(self):
        # просмотр каждого астероида по отдельности
        for i, asteroid in enumerate(self.asteroids):
            # удаление астероида который вышел за пределы экрана
            if not (0 <= asteroid.get_position()[0] <= WINDOW_WIDTH) or not (
                    0 <= asteroid.get_position()[1] <= WINDOW_HEIGHT):
                del self.asteroids[i]
            # столкновение астероида с главным героем
            if abs(asteroid.get_position()[0] - self.hero.get_position()[
                0]) < asteroid.radius + self.hero.radius and abs(
                    asteroid.get_position()[1] - self.hero.get_position()[1]) < asteroid.radius + self.hero.radius:
                # уничтожение астероида
                del self.asteroids[i]

                # нанесение урона главному герою
                self.hero.health -= asteroid.hp

                # вывод показателя здоровья главного героя в консоль
                print(f"HEALTH: {self.hero.health}")

            # движение астероида
            asteroid.set_position(
                (asteroid.get_position()[0] + asteroid.dx, asteroid.get_position()[1] + asteroid.dy))

    # движение баффов
    def move_buffs(self):
        for i, buff in enumerate(self.buffs):
            if not (0 <= buff.get_position()[1] <= WINDOW_HEIGHT):
                del self.buffs[i]

            # столкновение баффа с главным героем
            if abs(buff.get_position()[0] - self.hero.get_position()[0]) < buff.radius + self.hero.radius and abs(
                    buff.get_position()[1] - self.hero.get_position()[1]) < buff.radius + self.hero.radius:

                # активация баффа
                if buff.type == "HP":
                    self.hero.health += 1

                # удалаение баффа
                del self.buffs[i]

            # движение баффа
            buff.set_position(
                (buff.get_position()[0], buff.get_position()[1] + buff.speed))

    # добавить врага
    def add_enemy(self, enemy):
        if len(self.enemies) <= MAX_COUNT_OF_ENEMIES:
            self.enemies.append(enemy)

    # добавить астероид
    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)

    # добавить бафф
    def add_buff(self, buff):
        self.buffs.append(buff)


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # all_sprites = pygame.sprite.Group()
    hero = Hero((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    game = Game(hero)
    # all_sprites.add(labyrinth)
    # all_sprites.add(hero)
    # all_sprites.add(enemy)
    # часы
    clock = pygame.time.Clock()
    running = True
    # игровой цикл
    while running:
        for event in pygame.event.get():
            # закрытие окна
            if event.type == pygame.QUIT:
                running = False

        # герой жив
        if game.hero.health > 0:

            # движение всех динамичных объектов
            game.move_bullets()
            game.move_hero()
            game.move_enemies()
            game.move_asteroids()
            game.move_buffs()
            # генерация события например создание врага
            event = random.randint(0, 100000)
            # создание врага
            if event % 100 == 1:
                enemy = Enemy((random.randint(0, 600), random.randint(0, 50)))
                game.add_enemy(enemy)
            # создание астероида
            if event % 100 == 2:
                asteroid = Asteroid()
                game.add_asteroid(asteroid)
            if event % 1000 == 0:
                buff = Buff("HP")
                game.add_buff(buff)

            screen.fill((0, 0, 0))
            # применение спрайтов
            screen.blit(hero.render(screen)[0], hero.render(screen)[1])
            game.render(screen)
            clock.tick(FPS)

        # конец игры
        else:
            show_message(screen, "GAME OVER")
        # Обновление
        # all_sprites.update()
        # for sprite in all_sprites:
        #     sprite.x -= 5
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
