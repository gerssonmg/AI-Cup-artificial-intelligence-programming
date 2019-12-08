import model
class MyStrategy:
    def __init__(self):
        pass

    def get_action(self, unit, game, debug):
                
        # Replace this code with your own
        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        nearest_enemy =  min( filter(lambda u: u.player_id != unit.player_id, game.units), key=lambda u: distance_sqr(u.position, unit.position), default=None)
        nearest_weapon = min( filter(lambda box: isinstance( box.item, model.Item.Weapon), game.loot_boxes), key=lambda box: distance_sqr(box.position, unit.position), default=None)
        
        nearest_health = min( filter(lambda box: isinstance( box.item, model.Item.HealthPack), game.loot_boxes), key=lambda box: distance_sqr(box.position, unit.position), default=None)
        
        print("filter:", filter(lambda box: isinstance( box.item, model.Item.Weapon), game.loot_boxes))

        #print("model.Item::", model.Item)
        #print("game.loot_boxes::", game.loot_boxes)

        print("bullet:",game.bullets)

        target_pos = unit.position

        #Verifica se ja esta com 
        #Alguma arma, se não tiver
        #Ira em direção a arma
        #Se ja tiver uma arma, ira em direção
        #Ao Inimigo
        procurando_inimigo = False

        if unit.weapon is None and nearest_weapon is not None:
            target_pos = nearest_weapon.position
        elif unit.health < 90 and nearest_health is not None:
            target_pos = nearest_health.position            
        elif unit.weapon is not None and unit.weapon.typ == 2:
            if nearest_weapon is not None:
                target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position
            procurando_inimigo = True

        debug.draw(model.CustomData.Log("Txarget pos: {}".format(target_pos)))
        aim = model.Vec2Double(0, 0)
        if nearest_enemy is not None:
            aim = model.Vec2Double( nearest_enemy.position.x - unit.position.x, nearest_enemy.position.y - unit.position.y)

        jump = target_pos.y > unit.position.y
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        #if procurando_inimigo :
        #    jump = True
        
        '''
        print("unit" , unit)
        print("unit.mines" , unit.mines)
        print("unit.health" , unit.health)
        print("unit.weapon" , unit.weapon)
        print("unit.id" , unit.id)
        print("unit.jump_state" , unit.jump_state)
        print("unit.on_ground" , unit.on_ground)
        print("unit.on_ladder" , unit.on_ladder)
        print("unit.player_id" , unit.player_id)
        print("unit.position" , unit.position)
        print("unit.size" , unit.size)
        print("unit.stand" , unit.stand)
        print("unit.walked_right" , unit.walked_right)
        print("nearest_enemy" , nearest_enemy)
        print("nearest_weapon" , nearest_weapon)
        print("nearest_health" , nearest_health)
        print("nearest_health.postion:" , nearest_health.position)        
        print("target_pos.y" , target_pos.y)
        print("unit_pos.y" , unit.position.y)
        print("jump" , jump)    
        '''

        plat_mine_command = True
        #Deve ter pelo menos uma mina
        #E não pode estar na escada
        if unit.mines > 0 and unit.on_ladder == False:
            jump = False
            plat_mine_command = True
        
        #Troca de Arma
        #Se tiver com uma PISTOLA troca, por qualquer outra
        troca_arma = False
        if unit.weapon is not None:
            if unit.weapon.typ == 2 or unit.weapon.typ == 2:
                troca_arma = True
        
        
        
       ## if unit.health >= 90:
        ##    velocidade_deslocamento = target_pos.x - unit.position.x
        ##else :
        if True:
            velocidade_deslocamento = target_pos.x - unit.position.x
            if abs(velocidade_deslocamento) < 4 :
                velocidade_deslocamento *= 3
                if abs(velocidade_deslocamento) < 2 :
                    velocidade_deslocamento *= 5

        print("Velocity:",target_pos.x - unit.position.x)
        print("velocidade_deslocamento:",velocidade_deslocamento)

        return model.UnitAction(
            velocity=velocidade_deslocamento,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot=True,
            reload=False,
            swap_weapon=troca_arma,
            plant_mine=plat_mine_command)
