import model
class MyStrategy:
    def __init__(self):
        pass

    skill_jump_plat_variavel_global = 0
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

        desviar_de_bullet = False


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

            print("TODOS PERTO DE MIM:", health_mais_perto_de_mim)
            if len(health_mais_perto_de_mim) > 0:
                target_pos = min( health_mais_perto_de_mim,
                    key=lambda h_m_p_de_m: distance_sqr(h_m_p_de_m.position, unit.position),
                    default=None).position
                #target_pos = health_mais_perto_de_mim[0].position
            print("MAIS PERTO DE MIM:", target_pos)
           
        #############3#elif unit.weapon is not None and unit.weapon.typ == 2:
        elif unit.weapon is not None and unit.weapon.typ == 0 or unit.weapon.typ == 1:
            if nearest_weapon is not None:
                target_pos = nearest_weapon.position
        
        elif len(game.bullets) > 0:
            #Pega o Objeto inimigo
            for j in game.units:
                if unit.id != j.id:
                    inimigo =  j
            lista_bullet_inimigo = list(filter(lambda bull:  (bull.unit_id == inimigo.id), game.bullets))
            for i in lista_bullet_inimigo:
                print("INIMIGO BULLET:", i)

            if len(lista_bullet_inimigo) :
                #nearest_bullet = min( game.bullets, key=lambda bull: distance_sqr(bull.position, unit.position) )
                nearest_bullet = min( lista_bullet_inimigo, key=lambda bull: distance_sqr(bull.position, unit.position) )
                print("ALL BULLETS:", game.bullets)
                print("MIN BULLETS:", nearest_bullet)
                target_pos = nearest_bullet.position
                desviar_de_bullet = True

        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position
            procurando_inimigo = True

        print("POS:", target_pos)

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
                if game.level.tiles[i][ int(unit.position.y)] == model.Tile.WALL:
                    shooting_command = False
                    print("NOOO SHOOTING MAN")
                    break

        elif nearest_enemy.position.x < unit.position.x:
            for i in range(  int(nearest_enemy.position.x), int(unit.position.x) , 1 ):
                if game.level.tiles[i][ int(unit.position.y)] == model.Tile.WALL:
                    shooting_command = False
                    print("NO NO NO NO SHOOTING MAN")
                    break
     
        
        #Troca de Arma
        #Se tiver com uma ROCKET_LAUNCHER troca, por qualquer outra
        troca_arma = MyStrategy.troca_arma(unit)
        
        velocidade_deslocamento = MyStrategy.aumentar_velocidade(target_pos.x - unit.position.x)

        if desviar_de_bullet == True:
            velocidade_deslocamento *= -1
            jump = not jump

        jump_down = not jump
        skill_plat_form = MyStrategy.skill_up_platform(unit, target_pos, game, jump)
        if skill_plat_form == True:
            jump = False
            jump_down = False
        
        return model.UnitAction(
            velocity=velocidade_deslocamento,
            jump=jump,
            jump_down=jump_down,
            aim=aim,
            shoot= shooting_command,
            reload=False,
            swap_weapon=troca_arma,
            #plant_mine=plat_mine_command)
            plant_mine=False)

    def aumentar_velocidade(velocidade_deslocamento):

        velocidade_deslocamento *= 10
            
        '''if abs(velocidade_deslocamento) < 4 :
            velocidade_deslocamento *= 10
            if abs(velocidade_deslocamento) < 2 :
                velocidade_deslocamento *= 10
        '''
        return velocidade_deslocamento

    def troca_arma( unit ):

        troca_arma = False
        if unit.weapon is not None:
            if unit.weapon.typ == 0:
            ###########if unit.weapon.typ == 2:
                troca_arma = True

        return troca_arma

    def skill_up_platform(unit, target, game, jump):
        #Deve verificar se esta sobre uma platform
        #Se estiver, e seu alvo estiver mais acima, ele deve parar de pular
        #E deve pular partindo dessa nova plataforma
        print("ABAIXO:", game.level.tiles[ int(unit.position.x) ][int(unit.position.y - 1)])

        # Replace this code with your own
        def distance_sqrrr(a, b):
            return (a.x - b.x) ** 2 + (a.y - int(b.y-1)) ** 2
        d = distance_sqrrr ( unit.position, unit.position)
        print("DISTANCIA BAIXO:", d)
        
        print("skilll_01:", MyStrategy.skill_jump_plat_variavel_global)
        if game.level.tiles[ int(unit.position.x) ][int(unit.position.y - 1)] == model.Tile.PLATFORM and jump == True and MyStrategy.skill_jump_plat_variavel_global != 1:
            print("NO JUMP PLAT")
            print("AND NO DOWN PLAT")
            MyStrategy.skill_jump_plat_variavel_global = 1
            print("skilll_02:", MyStrategy.skill_jump_plat_variavel_global)
            return True
        
        if game.level.tiles[ int(unit.position.x) ][int(unit.position.y - 1)] != model.Tile.PLATFORM:
            print("skilll_03:", MyStrategy.skill_jump_plat_variavel_global)
            MyStrategy.skill_jump_plat_variavel_global = 0
        return False
        
    def skill_plant_mine():
        plat_mine_command = True
        #Deve ter pelo menos uma mina
        #E não pode estar na escada
        if unit.mines > 0 and unit.on_ladder == False:
            if game.level.tiles[ int(unit.position.x) ][int(unit.position.y - 1)] == model.Tile.WALL:
                jump = False
                plat_mine_command = True
        return 0