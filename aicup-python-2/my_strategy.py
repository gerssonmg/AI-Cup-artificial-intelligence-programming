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

            #Se tiver outro pacote mais perto de mim
            #do que do inimigo, ira atraz dele

            #Pega o Objeto inimigo
            for j in game.units:
                if unit.id != j.id:
                    inimigo =  j        
            print("BEGIN FOR")         
            health_mais_perto_de_mim = []       
            #Itera em todos os pacotes
            for i in game.loot_boxes:        
               #Se o pacote for de vida
                if isinstance(i.item, model.Item.HealthPack):
                    #print("loots.item:" , i)
                
                    #To mais perto que o inimigo
                    #Da vida
                    if distance_sqr(i.position, unit.position) < distance_sqr(i.position, inimigo.position):
                        health_mais_perto_de_mim.append(i)
            if len(health_mais_perto_de_mim) > 0:
                target_pos = health_mais_perto_de_mim[0].position
        
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

        #print("AIM:", aim)
        print("unit.position.x:", unit.position.x)
        print("unit.position.y:", unit.position.y)
        
        jump = target_pos.y > unit.position.y
        #Caso chegue em uma parede, ele pula
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True

        #posição do alvo maior que a posição minha atual
        shooting_command = True

        if nearest_enemy.position.x > unit.position.x:
            for i in range( int(unit.position.x) , int(nearest_enemy.position.x), 1 ):
                #print("game__tiles__middle::" , game.level.tiles[i][ int(unit.position.y)] )
                if game.level.tiles[i][ int(unit.position.y)] == model.Tile.WALL:
                    shooting_command = False
                    print("NOOO SHOOTING MAN")
                    break

        elif nearest_enemy.position.x < unit.position.x:
            for i in range(  int(nearest_enemy.position.x), int(unit.position.x) , 1 ):
                #print("game__tiles__middle::" , game.level.tiles[i][ int(unit.position.y)] )
                if game.level.tiles[i][ int(unit.position.y)] == model.Tile.WALL:
                    shooting_command = False
                    print("NO NO NO NO SHOOTING MAN")
                    break
     
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
        
        if True:
            velocidade_deslocamento = target_pos.x - unit.position.x            
            velocidade_deslocamento *= 30
            
            if abs(velocidade_deslocamento) < 4 :
                velocidade_deslocamento *= 3
                if abs(velocidade_deslocamento) < 2 :
                    velocidade_deslocamento *= 5
        
        return model.UnitAction(
            velocity=velocidade_deslocamento,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot= shooting_command,
            reload=False,
            swap_weapon=troca_arma,
            plant_mine=plat_mine_command)
