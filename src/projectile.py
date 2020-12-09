from sprite import Sprite
from window_settings import *


class Projectile:
    def __init__(self):
        self.muzzleflash = Sprite(
            "./assets/sprites/EXTRAS/MuzzleFlash.png", 1, upscale=2
        )
        self.bsprite = Sprite("./assets/sprites/EXTRAS/BulletStream.png", 1, upscale=2)
        self.shoot_sfx = pygame.mixer.Sound("assets/sfx/game/shoot.wav")
        self.bullet_list = []
        self.speed = PX(0.005)

    def update(self, sprites, shot_fired):
        sprites.remove(self.muzzleflash)
        if shot_fired:
            self.muzzleflash.update_sprite(*shot_fired[0])
            self.muzzleflash.move(*shot_fired[1])
            self.shoot_sfx.play()
            self.addbullet(self.muzzleflash)
            sprites.add(self.muzzleflash)

        self.updatebullets(sprites)

        return sprites

    def addbullet(self, shot_fired):
        new_bullet = self.bsprite
        if self.muzzleflash.flip:
            x = shot_fired.rect.center[0] - PX(0.06)
        else:
            x = shot_fired.rect.center[0] + PX(0.06)
        y = shot_fired.rect.center[1]
        new_bullet.update_sprite(0, self.muzzleflash.flip)
        new_bullet.move(x, y)
        self.bullet_list.append(new_bullet)

    def updatebullets(self, sprites):
        for bullet in self.bullet_list:
            sprites.remove(bullet)
            if bullet.flip:
                bullet.move(-self.speed)
            else:
                bullet.move(self.speed)
            sprites.add(bullet)
