from flask import Flask, render_template, jsonify, request, url_for
import cv2
import mediapipe as mp
import numpy as np
import pickle
import base64
import random
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Cargar modelos
#Modelo Abecedario
model_dict = pickle.load(open('./model/model.p', 'rb'))  
model = model_dict['model']
#Modelo Saludos
models_dict = pickle.load(open('./model/models.p', 'rb'))
models = models_dict['model']
#Modelo Emociones
modelr_dict = pickle.load(open('./model/modelr.p', 'rb'))
modelr = modelr_dict['model']
#Modelo Presentacion
modelp_dict = pickle.load(open('./model/modelp.p', 'rb')) 
modelp = modelp_dict['model'] 
#Modelo Negación y Existencia
modeln_dict = pickle.load(open('./model/modeln.p', 'rb'))
modeln = modeln_dict['model']
#Modelo Ubicación
modelu_dict = pickle.load(open('./model/modelu.p', 'rb'))
modelu_dict = modelu_dict['model']
#Modelo Problemas
modelps_dict = pickle.load(open('./model/modelps.p', 'rb'))
modelps = modelps_dict['model']
#Modelo Estados de Ánimo
modeles_dict = pickle.load(open('./model/modeles.p', 'rb'))
modeles = modeles_dict['model']
#Modelo Conducta
modelc_dict = pickle.load(open('./model/modelc.p', 'rb'))
modelc = modelc_dict['model']
#Modelo Salud y Bienestar
modelsb_dict = pickle.load(open('./model/modelsb.p', 'rb'))
modelsb = modelsb_dict['model']
#Modelo Familia
modelf_dict = pickle.load(open('./model/modelf.p', 'rb'))
modelf = modelf_dict['model']
#Modelo Comunicación
modelcel_dict = pickle.load(open('./model/modelscei.p', 'rb'))
modelcel = modelcel_dict['model']
#Modelo Tiempo
modelt_dict = pickle.load(open('./model/modelt.p', 'rb'))
modelt = modelt_dict['model']
#Modelo verbos
modelv_dict = pickle.load(open('./model/modelv.p', 'rb'))
modelv = modelv_dict['model']
#Modelo Descripcion
modeldc_dict = pickle.load(open('./model/modeldc.p', 'rb'))
modeldc = modeldc_dict['model']
#Modelo preguntas
modelpe_dict = pickle.load(open('./model/modelpe.p', 'rb'))
modelpe = modelpe_dict['model']

# Diccionarios de etiquetas
#Etiquetas del modelo Abecedario
labels_dict = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',12:'ll',13:'m',14:'n',15:'ñ',16:'o',17:'p',18:'q',19:'r',20:'rr',21:'s',22:'t',23:'u',24:'v',25:'w',26:'x',27:'y',28:'z'}
#Etiquetas del modelo Saludos
labels_dicts = { 0: 'Hola', 1: 'Buenos dias', 2: 'Buenas tardes', 3: 'Buenas noches', 4: '¿Como estas?',}
#Etiquetas del modelo Emociones
labels_dictr = { 0: 'Bien',  1: 'Mal',  2: 'Más o menos',  3: 'Enojado',  4: 'Triste',  5: 'Serio',  6: 'Apenado',  7: 'Contento',  8: 'Feliz',  9: 'Molesto', 10: 'Hambriento',  11: 'Bailarín',  12: 'Malo',  13: 'Bueno',  14: 'Alegre',  15: 'Llorar' }
#Etiquetas del modelo Presentación
labels_dictp = { 0: 'Nombre',  1: 'Seña'}
#Etiquetas del modelo Negación y Existencia
labels_dictn = { 0: 'No sé',  1: 'Nada/ De nada',  2: 'Nadie',  3: 'No hay',  4: 'No necesito'}
#Etiquetas del modelo Ubicación
labels_dictu = { 0: '¿Donde?',  1: 'Lugar',  2: 'Ciudad',  3: '¿Donde vives?',  4: 'Escuela',  5: 'Salón',  6: 'Salir'}
#Etiquetas del modelo Problemas
labels_dictps = {0:'Emergencia',1:'Cuidado',2:'Peligro',3:'Problema',4:'Accidente',5:'Culpa',6:'Sucio',7:'Basura',8:'No sirve',9:'Memoria',10:'Descompuesto',11:'Reparar',12:'Prohibido',13:'Error'}
# Etiquetas del modelo Estados de Ánimo
labels_dictes = {0:'Tranquilo', 1:'Distraído', 2:'Confianza', 3:'Confundido', 4:'Sentir', 5:'Quiero', 6:'No quiero', 7:'Mejor', 8:'Peor', 9:'Grave', 10:'Me siento débil'}
#Etiquetas del modelo Conducta
labels_dictc = {0:'Regañar', 1:'Castigar', 2: 'Obedecer', 3: 'Travieso', 4: 'Educado', 5: 'Responsable', 6: 'Respeto', 7: 'Tramposo', 8: 'No hagas caso', 9: 'Grosero', 10: 'Burla', 11: 'Criticar', 12: 'Evitar', 13: 'Participar', 14: 'Levantar la mano', 15: 'Permiso', 16: 'Quitar', 17: 'Ni modo', 18: 'Aguantate', 19: 'Reglas', 20: 'Fila', 21: 'Silencio', 22: 'Callate', 23: 'Necio', 24: 'No gritar', 25: 'Siéntate', 26: 'Ponte de pie', 27: 'No correr', 28: 'No empujar', 29: 'Pelear/golpear', 30: 'Bullying', 31: 'Perdón', 32: 'Disculpa', 33: 'Ya!'}
#Etiquetas del modelo Salud y Bienestar
labels_dictsb = {0:'Enfermo', 1:'Gripa', 2:'Bañate', 3:'Desayunar', 4:'Almuerzo',5:'Comer'}
#Etiquetas del modelo Familia
labels_dictf = {0: 'Mamá', 1: 'Papá', 2: 'Maestro', 3: 'Maestra', 4: 'Director', 5: 'Directora', 6: 'Jefe', 7: 'Abuelo', 8: 'Abuela', 9: 'Tío', 10: 'Tia', 11: 'Primo', 12: 'Prima', 13: 'Hermano', 14: 'Hermana', 15: 'Amigo', 16: 'Amiga', 17: 'Novio', 18: 'Vecino', 19: 'Vecina'}
#Etiquetas del modelo Comunicación
labels_dictcel = {0: 'Atención', 1: 'Fijate', 2: 'Mentira/mentiroso', 3: 'Verdad', 4: 'Falso..', 5: 'Dime', 6: 'Estar de acuerdo', 7: '¿Puedo?', 8: 'No puedo', 9: 'Basta!', 10: 'Pregunta', 11: 'Tu pregunta', 12: 'A mi pregúntame', 13: 'A todos le preguntarée', 14: '¿Si me entendiste?', 15: 'No entendiste', 16: 'Avisar', 17: 'Engañar'}
#Etiquetas del modelo tiempo
labels_dictt = {0: '¿Cuándo?', 1: '¿Cuántos?', 2: 'Tiempo', 3: 'Tarde', 4: 'Poco', 5: 'Mucho', 6: 'Menos', 7: 'Otra vez/repetir', 8: 'Otro'}
#Etiquetas del modelo verbos
labels_dictv = {0: 'Guardar cosas', 1: 'Ordena/organiza', 2: 'Limpiar', 3: 'Ver', 4: 'Mira', 5: 'Decir', 6: 'Recordar', 7: 'Olvidar', 8: 'Hablar', 9: 'Platicar', 10: 'Aprender', 11: 'Enseñar', 12: 'Bailar', 13: 'Tarea', 14: 'Estudiar', 15: 'Pensar', 16: 'Saber', 17: 'Hacer', 18: 'Usar', 19: 'Trabajar', 20: 'Dormir', 21: 'Despertar', 22: 'Prestar'}
#Etiquetas del modelo Descripcion
labels_dictdc = {0:'Feo', 1:'Bonito', 2:'Tu ropa Sucia', 3:'Tu ropa limpia', 4:'Bien', 5:'Mal', 6:'Me gusta',7:'No me gusta' ,8:'Lento', 9:'Rapido'}
#Etiquetas del modelo Preguntas
labelspe_dict = {0:'¿Qué haces?', 1:'¿Para?', 2:'¿Para qué?', 3:'¿Por qué?', 4:'¿Qué pasó?', 5:'¿Cómo?', 6:'¿Qué significa?', 7:'¿Qué necesitas?'}

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Listas de imágenes y videos
sign_images = ['a.jpeg','b.jpeg','c.jpeg','d.jpeg','e.jpeg','f.jpeg','g.jpeg','h.jpeg','i.jpeg','j.jpeg','k.jpeg','l.jpeg','ll.jpeg','m.jpeg','n.jpeg','ñ.jpeg','o.jpeg','p.jpeg','q.jpeg','r.jpeg','rr.jpeg','s.jpeg','t.jpeg','u.jpeg','v.jpeg','w.jpeg','x.jpeg','y.jpeg','z.jpeg']
sign_videos = ['hola.mp4', 'buenos_dias.mp4', 'buenas_tardes.mp4', 'buenas_noches.mp4', 'comoestas.mp4']
emotion_videos = ['bien.mp4', 'mal.mp4', 'mas_o_menos.mp4', 'enojado.mp4', 'triste.mp4', 'serio.mp4', 'apenado.mp4', 'contento.mp4', 'feliz.mp4', 'molesto.mp4', 'hambriento.mp4', 'bailarin.mp4', 'malo.mp4', 'bueno.mp4', 'alegre.mp4', 'llorar.mp4']
presentation_videos = ['nombre.mp4', 'senha.mp4']
negation_videos = ['no_se.mp4', 'nada.mp4', 'nadie.mp4', 'no_hay.mp4', 'no_necesito.mp4']
location_videos = ['donde.mp4', 'lugar.mp4', 'ciudad.mp4', 'donde_vives.mp4', 'escuela.mp4', 'salon.mp4', 'salir.mp4']
problem_videos = ['emergencia.mp4', 'cuidado.mp4', 'peligro.mp4', 'problema.mp4', 'accidente.mp4', 'culpa.mp4', 'sucio.mp4', 'basura.mp4', 'no_sirve.mp4', 'memoria.mp4', 'descompuesto.mp4', 'reparar.mp4', 'prohibido.mp4', 'error.mp4']
moods_videos = ['tranquilo.mp4', 'distraído.mp4', 'confianza.mp4', 'confundido.mp4', 'sentir.mp4', 'quiero.mp4', 'no_quiero.mp4', 'mejor.mp4', 'peor.mp4', 'grave.mp4', 'me_siento_débil.mp4']
conduct_videos = ['regañar.mp4', 'castigar.mp4', 'obedecer.mp4', 'travieso.mp4', 'educado.mp4', 'responsable.mp4', 'respeto.mp4', 'tramposo.mp4', 'no_hagas_caso.mp4', 'grosero.mp4', 'burla.mp4', 'criticar.mp4', 'evitar.mp4', 'participar.mp4', 'levantar_la_mano.mp4', 'permiso.mp4', 'quitar.mp4', 'ni_modo.mp4', 'aguantate.mp4', 'reglas.mp4', 'fila.mp4', 'silencio.mp4', 'callate.mp4', 'necio.mp4', 'no_gritar.mp4', 'sientate.mp4', 'ponte_de_pie.mp4', 'no_correr.mp4', 'no_empujar.mp4','pelear.mp4','bullying.mp4','perdon.mp4','disculpa.mp4','ya_mp4']
health_videos = ['enfermo.mp4', 'gripa.mp4', 'banate.mp4', 'desayunar.mp4', 'almuerzo.mp4', 'comer.mp4']
family_videos = ['mama.mp4', 'papa.mp4', 'maestro.mp4', 'maestra.mp4', 'director.mp4', 'directora.mp4', 'jefe.mp4', 'abuelo.mp4', 'abuela.mp4', 'tio.mp4', 'tia.mp4', 'primo.mp4', 'prima.mp4', 'hermano.mp4', 'hermana.mp4', 'amigo.mp4', 'amiga.mp4', 'novio.mp4', 'vecino.mp4', 'vecina.mp4']
comunication_videos = ['atencion.mp4', 'fijate.mp4', 'mentira.mp4', 'verdad.mp4', 'falso.mp4', 'dime.mp4', 'estar_de_acuerdo.mp4', 'puedo.mp4', 'no_puedo.mp4', 'basta.mp4', 'pregunta.mp4', 'tu_pregunta.mp4', 'a_mi_preguntame.mp4', 'a_todos_le_preguntare.mp4', 'si_me_entendiste.mp4', 'no_entendiste.mp4', 'avisar.mp4', 'enganar.mp4']
time_videos = ['cuando.mp4', 'cuantos.mp4', 'tiempo.mp4', 'tarde.mp4', 'poco.mp4', 'mucho.mp4', 'menos.mp4', 'otra_vez.mp4', 'otro.mp4']
verbs_videos = ['guardar_cosas.mp4', 'ordena_organizar.mp4', 'limpiar.mp4', 'ver.mp4', 'mira.mp4', 'decir.mp4', 'recordar.mp4', 'olvidar.mp4', 'hablar.mp4', 'platicar.mp4', 'aprender.mp4', 'enseñar.mp4', 'bailar.mp4', 'tarea.mp4', 'estudiar.mp4', 'pensar.mp4', 'saber.mp4', 'hacer.mp4', 'usar.mp4', 'trabajar.mp4', 'dormir.mp4', 'despertar.mp4', 'prestar.mp4']
description_videos = ['feo.mp4', 'bonito.mp4', 'tu_ropa_sucia.mp4', 'tu_ropa_limpia.mp4', 'bien.mp4', 'mal.mp4', 'me_gusta.mp4', 'no_me_gusta.mp4', 'lento.mp4', 'rapido.mp4']
questions_videos = ['que_haces.mp4', 'para.mp4', 'para_que.mp4', 'por_que.mp4', 'que_paso.mp4', 'como.mp4', 'que_significa.mp4', 'que_necesitas.mp4']

# Obtener índices válidos
valid_indices = list(range(len(sign_images)))
valids_indices = list(range(len(sign_videos)))
emotion_indices = list(range(len(emotion_videos)))
presentation_indices = list(range(len(presentation_videos)))
negation_indices = list(range(len(negation_videos)))
location_indices = list(range(len(location_videos)))
problem_indices = list(range(len(problem_videos)))
moods_indices = list(range(len(moods_videos)))
conduct_indices = list(range(len(conduct_videos)))
health_indices = list(range(len(health_videos)))
family_indices = list(range(len(family_videos)))
comunication_indices = list(range(len(conduct_videos)))
time_indices = list(range(len(time_videos)))
verbs_indices = list(range(len(verbs_videos)))
description_indices = list(range(len(description_videos)))
questions_indices = list(range(len(questions_videos)))

def new_random_image():
    random_index = random.choice(valid_indices)
    return sign_images[random_index], labels_dict[random_index]

# Variables globales de estado
current_image, current_target = new_random_image()
current_video_index = 0
current_emotion_index = 0
current_presentation_index = 0  
current_negation_index = 0
current_location_index = 0
current_problem_index = 0
current_mood_index = 0
current_conduct_index = 0
current_health_index = 0
current_family_index = 0
current_comunication_index = 0
current_time_index = 0
current_verb_index = 0
current_description_index = 0
current_question_index = 0

# Inicializar variables para videos de presentación
@app.route('/gestos')
def gestos():
    return render_template('deteccion.html')

@app.route('/gestos/saludos')
def gestos_saludos():
    return render_template('deteccionsaludos.html')

@app.route('/gestos/emociones')
def gestos_emociones():
    return render_template('deteccionemociones.html')

@app.route('/gestos/presentacion')
def gestos_presentacion():
    return render_template('deteccionpresentacion.html')

@app.route('/gestos/negacion')
def gestos_negacion():
    return render_template('deteccionnegacion.html')

@app.route('/gestos/ubicacion')
def gestos_location():
    return render_template('deteccionubicacion.html')

@app.route('/gestos/problemas')
def gestos_problemas():
    return render_template('deteccionproblemas.html')

@app.route('/gestos/estadosanimo')
def gestos_mood():
    return render_template('deteccionestadosa.html')

@app.route('/gestos/conducta')
def gestos_conduct():
    return render_template('deteccionconducta.html')

@app.route('/gestos/salud')
def gestos_health():
    return render_template('deteccionsalud.html')

@app.route('/gestos/familia')
def gestos_family():
    return render_template('deteccionfamilia.html')

@app.route('/gestos/comunicacion')
def gestos_comunicacion():
    return render_template('deteccioncomunicacion.html')

@app.route('/gestos/tiempo')
def gestos_time():
    return render_template('detecciontiempo.html')

@app.route('/gestos/verbos')
def gestos_verbs():
    return render_template('deteccionverbos.html')

@app.route('/gestos/descripcion')
def gestos_description():
    return render_template('detecciondescripcion.html')

@app.route('/gestos/preguntas')
def gestos_questions():
    return render_template('deteccionpreguntas.html')

# Inicializamos current_target en None para evitar valores residuales
current_image, current_target = None, None
current_video, current_target = None, None
current_emotion, current_emotion_target = None, None
current_presentation, current_presentation_target = None, None  # Inicializado variables para presentación
current_negation, current_negation_target = None, None 
current_location, current_location_target = None, None  
current_problem, current_problem_target = None, None  
current_mood, current_mood_target = None, None
current_conduct, current_conduct_target = None, None
current_health, current_health_target = None, None
current_family, current_family_target = None, None
current_comunication, current_comunication_target = None, None
current_time, current_time_target = None, None
current_verbs, current_verbs_target = None, None
current_description, current_description_target = None, None
current_question, current_question_target = None, None

# Deteccion abecedario
def new_ordered_video():
    global current_video_index
    if current_video_index < len(sign_videos):
        video = sign_videos[current_video_index]
        target = labels_dicts[current_video_index]
        current_video_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_video_index = 0
        return sign_videos[current_video_index], labels_dicts[current_video_index]

# Deteccion de emociones
def new_ordered_emotion():
    global current_emotion_index
    if current_emotion_index < len(emotion_videos):
        video = emotion_videos[current_emotion_index]
        target = labels_dictr[current_emotion_index]
        current_emotion_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_emotion_index = 0
        return emotion_videos[current_emotion_index], labels_dictr[current_emotion_index]

# Deteccion presentacion
def new_ordered_presentation():
    global current_presentation_index
    if current_presentation_index < len(presentation_videos):
        video = presentation_videos[current_presentation_index]
        target = labels_dictp[current_presentation_index]
        current_presentation_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_presentation_index = 0
        return presentation_videos[current_presentation_index], labels_dictp[current_presentation_index]
    
# Deteccion negación y existencia
def new_ordered_negation():
    global current_negation_index
    if current_negation_index < len(negation_videos):
        video = negation_videos[current_negation_index]
        target = labels_dictn[current_negation_index]
        current_negation_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_negation_index = 0
        return negation_videos[current_negation_index], labels_dictn[current_negation_index]
   
# Deteccion ubicacion
def new_ordered_location():
    global current_location_index
    if current_location_index < len(location_videos):
        video = location_videos[current_location_index]
        target = labels_dictu[current_location_index]
        current_location_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_location_index = 0
        return location_videos[current_location_index], labels_dictu[current_location_index]

# Deteccion problemas
def new_ordered_problem():
    global current_problem_index
    if current_problem_index < len(problem_videos):
        video = problem_videos[current_problem_index]
        target = labels_dictps[current_problem_index]
        current_problem_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_problem_index = 0
        return problem_videos[current_problem_index], labels_dictps[current_problem_index]

# Deteccion estados de ánimo
def new_ordered_mood():
    global current_mood_index
    if current_mood_index < len(moods_videos):
        video = moods_videos[current_mood_index]
        target = labels_dictes[current_mood_index]
        current_mood_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_mood_index = 0
        return moods_videos[current_mood_index], labels_dictes[current_mood_index]

# Deteccion conducta
def new_ordered_conduct():
    global current_conduct_index
    if current_conduct_index < len(conduct_videos):
        video = conduct_videos[current_conduct_index]
        target = labels_dictc[current_conduct_index]
        current_conduct_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_conduct_index = 0
        return conduct_videos[current_conduct_index], labels_dictc[current_conduct_index] 
    
# Deteccion salud
def new_ordered_health():
    global current_health_index
    if current_health_index < len(health_videos):
        video = health_videos[current_health_index]
        target = labels_dictsb[current_health_index]
        current_health_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_health_index = 0
        return health_videos[current_health_index], labels_dictsb[current_health_index] 

# Deteccion familia
def new_ordered_family():
    global current_family_index
    if current_family_index < len(family_videos):
        video = family_videos[current_family_index]
        target = labels_dictf[current_family_index]
        current_family_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_family_index = 0
        return family_videos[current_family_index], labels_dictf[current_family_index] 

# Deteccion comunicacion
def new_ordered_comunication():
    global current_comunication_index
    if current_comunication_index < len(comunication_videos):
        video = comunication_videos[current_comunication_index]
        target = labels_dictcel[current_comunication_index]
        current_comunication_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_comunication_index = 0
        return comunication_videos[current_comunication_index], labels_dictcel[current_comunication_index]

# Deteccion tiempo
def new_ordered_time():
    global current_time_index
    if current_time_index < len(time_videos):
        video = time_videos[current_time_index]
        target = labels_dictt[current_time_index]
        current_time_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_time_index = 0
        return time_videos[current_time_index], labels_dictt[current_time_index]

# Deteccion verbos
def new_ordered_verbs():
    global current_verb_index
    if current_verb_index < len(verbs_videos):
        video = verbs_videos[current_verb_index]
        target = labels_dictv[current_verb_index]
        current_verb_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_verb_index = 0
        return verbs_videos[current_verb_index], labels_dictv[current_verb_index]

# Deteccion descripcion
def new_ordered_description():
    global current_description_index
    if current_description_index < len(description_videos):
        video = description_videos[current_description_index]
        target = labels_dictdc[current_description_index]
        current_description_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_description_index = 0
        return description_videos[current_description_index], labels_dictdc[current_description_index]
    
# Deteccion preguntas
def new_ordered_question():
    global current_question_index
    if current_question_index < len(questions_videos):
        video = questions_videos[current_question_index]
        target = labelspe_dict[current_question_index]
        current_question_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_question_index = 0
        return questions_videos[current_question_index], labelspe_dict[current_question_index]
    
#Imagen aleatoria Abecedario
@app.route('/gestos/get_current_image')
def get_current_image():
    global current_image, current_target
    current_image, current_target = new_random_image()  # Siempre obtiene una nueva imagen
    try:
        image_url = url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True)
        return jsonify({'image_url': image_url, 'target': current_target, 'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
# Videos aleatorios Saludos
@app.route('/gestos/saludos/get_current_video')
def get_current_video():
    global current_video, current_target
    current_video, current_target = new_ordered_video()  # Obtener el siguiente video en orden
    try:
        video_url = url_for('static', filename=f'videos/greetings/{current_video}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_target, 'status': 'success', 'is_last': current_video_index >= len(sign_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Emociones
@app.route('/gestos/emociones/get_current_video')
def get_current_emotion_video():
    global current_emotion, current_emotion_target
    current_emotion, current_emotion_target = new_ordered_emotion()  # Obtener el siguiente video de emoción
    try:
        video_url = url_for('static', filename=f'videos/emotions/{current_emotion}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_emotion_target, 'status': 'success', 'is_last': current_emotion_index >= len(emotion_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Presentación
@app.route('/gestos/presentacion/get_current_video')
def get_current_presentation_video():  # Corregido el nombre de la función
    global current_presentation, current_presentation_target
    current_presentation, current_presentation_target = new_ordered_presentation()  
    try:
        video_url = url_for('static', filename=f'videos/presentation/{current_presentation}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_presentation_target, 'status': 'success', 'is_last': current_presentation_index >= len(presentation_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Negación
@app.route('/gestos/negacion/get_current_video')
def get_current_negation_video():  # Corregido el nombre de la función
    global current_negation, current_negation_target
    current_negation, current_negation_target = new_ordered_negation()  
    try:
        video_url = url_for('static', filename=f'videos/negation/{current_negation}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_negation_target, 'status': 'success', 'is_last': current_negation_index >= len(negation_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Ubicación
@app.route('/gestos/ubicacion/get_current_video')
def get_current_location_video():  # Corregido el nombre de la función
    global current_location, current_location_target
    current_location, current_location_target = new_ordered_location()  
    try:
        video_url = url_for('static', filename=f'videos/location/{current_location}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_location_target, 'status': 'success', 'is_last': current_location_index >= len(location_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Problemas
@app.route('/gestos/problemas/get_current_video')
def get_current_problem_video():  # Corregido el nombre de la función
    global current_problem, current_problem_target
    current_problem, current_problem_target = new_ordered_problem()
    try:
        video_url = url_for('static', filename=f'videos/problem/{current_problem}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_problem_target, 'status': 'success', 'is_last': current_problem_index >= len(problem_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Estados de Ánimo
@app.route('/gestos/estadosanimo/get_current_video')
def get_current_mood_video():  # Corregido el nombre de la función
    global current_mood, current_mood_target
    current_mood, current_mood_target = new_ordered_mood() 
    try:
        video_url = url_for('static', filename=f'videos/moods/{current_mood}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_mood_target, 'status': 'success', 'is_last': current_mood_index >= len(moods_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Conducta
@app.route('/gestos/conducta/get_current_video')
def get_current_conduct_video():  # Corregido el nombre de la función
    global current_conduct, current_conduct_target
    current_conduct, current_conduct_target = new_ordered_conduct() 
    try:
        video_url = url_for('static', filename=f'videos/conduct/{current_conduct}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_conduct_target, 'status': 'success', 'is_last': current_conduct_index >= len(conduct_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
# Videos aleatorios Salud
@app.route('/gestos/salud/get_current_video')
def get_current_health_video():  # Corregido el nombre de la función
    global current_health, current_health_target
    current_health, current_health_target = new_ordered_health() 
    try:
        video_url = url_for('static', filename=f'videos/health/{current_health}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_health_target, 'status': 'success', 'is_last': current_health_index >= len(health_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Familia
@app.route('/gestos/familia/get_current_video')
def get_current_family_video():  # Corregido el nombre de la función
    global current_family, current_family_target
    current_family, current_family_target = new_ordered_family() 
    try:
        video_url = url_for('static', filename=f'videos/family/{current_family}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_family_target, 'status': 'success', 'is_last': current_family_index >= len(family_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Comunicacion
@app.route('/gestos/comunicacion/get_current_video')
def get_current_comunication_video():  # Corregido el nombre de la función
    global current_comunication, current_comunication_target
    current_comunication, current_comunication_target = new_ordered_comunication()  
    try:
        video_url = url_for('static', filename=f'videos/comunication/{current_comunication}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_comunication_target, 'status': 'success', 'is_last': current_comunication_index >= len(comunication_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Tiempo
@app.route('/gestos/tiempo/get_current_video')
def get_current_time_video():  # Corregido el nombre de la función
    global current_time, current_time_target
    current_time, current_time_target = new_ordered_time() 
    try:
        video_url = url_for('static', filename=f'videos/time/{current_time}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_time_target, 'status': 'success', 'is_last': current_time_index >= len(time_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Verbos
@app.route('/gestos/verbos/get_current_video')
def get_current_verb_video():  # Corregido el nombre de la función
    global current_verbs, current_verbs_target
    current_verbs, current_verbs_target = new_ordered_verbs() 
    try:
        video_url = url_for('static', filename=f'videos/verbs/{current_verbs}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_verbs_target, 'status': 'success', 'is_last': current_verb_index >= len(verbs_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Descripcion
@app.route('/gestos/descripcion/get_current_video')
def get_current_description_video():  # Corregido el nombre de la función
    global current_description, current_description_target
    current_description, current_description_target = new_ordered_description() 
    try:
        video_url = url_for('static', filename=f'videos/description/{current_description}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_description_target, 'status': 'success', 'is_last': current_description_index >= len(description_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Videos aleatorios Preguntas
@app.route('/gestos/preguntas/get_current_video')
def get_current_question_video():  # Corregido el nombre de la función
    global current_question, current_question_target
    current_question, current_question_target = new_ordered_question()
    try:
        video_url = url_for('static', filename=f'videos/questions/{current_question}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_question_target, 'status': 'success', 'is_last': current_question_index >= len(questions_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
      
# Boton salto abecedario
@app.route('/gestos/skip', methods=['POST'])
def skip_image():
    global current_image, current_target
    current_image, current_target = new_random_image()
    return jsonify({'status': 'success', 'image_url': url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True), 'target': current_target})

# Boton salto saludos
@app.route('/gestos/saludos/skip', methods=['POST'])
def skip_video():
    global current_video, current_target
    current_video, current_target = new_ordered_video()  # Obtener el siguiente video en orden
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/greetings/{current_video}', _external=True), 'target': current_target})

# Boton salto emociones
@app.route('/gestos/emociones/skip', methods=['POST'])
def skip_emotion_video():
    global current_emotion, current_emotion_target
    current_emotion, current_emotion_target = new_ordered_emotion()  # Obtener el siguiente video de emociones
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/emotions/{current_emotion}', _external=True), 'target': current_emotion_target})

# Boton salto presentacion
@app.route('/gestos/presentacion/skip', methods=['POST'])
def skip_presentation_video():
    global current_presentation, current_presentation_target
    current_presentation, current_presentation_target = new_ordered_presentation() 
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/presentation/{current_presentation}', _external=True), 'target': current_presentation_target})

# Boton salto negación
@app.route('/gestos/negacion/skip', methods=['POST'])
def skip_negation_video():
    global current_negation, current_negation_target  # Corregido el nombre de la variable
    current_negation, current_negation_target = new_ordered_negation()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/negation/{current_negation}', _external=True), 'target': current_negation_target})

# Boton salto ubicación
@app.route('/gestos/ubicacion/skip', methods=['POST'])
def skip_location_video():
    global current_location, current_location_target  # Corregido el nombre de la variable
    current_location, current_location_target = new_ordered_location()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/location/{current_location}', _external=True), 'target': current_location_target})

# Boton salto problemas
@app.route('/gestos/problemas/skip', methods=['POST'])
def skip_problem_video():
    global current_problem, current_problem_target  # Corregido el nombre de la variable
    current_problem, current_problem_target = new_ordered_problem()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/problemas/{current_problem}', _external=True), 'target': current_problem_target})

# Boton salto estados de ánimo
@app.route('/gestos/estadosanimo/skip', methods=['POST'])
def skip_mood_video():
    global current_mood, current_mood_target  # Corregido el nombre de la variable
    current_mood, current_mood_target = new_ordered_mood()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/moods/{current_mood}', _external=True), 'target': current_mood_target})

# Boton salto conducta
@app.route('/gestos/conducta/skip', methods=['POST'])
def skip_conduct_video():
    global current_conduct, current_conduct_target  # Corregido el nombre de la variable
    current_conduct, current_conduct_target = new_ordered_conduct()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/conduct/{current_conduct}', _external=True), 'target': current_conduct_target})

# Boton salto salud
@app.route('/gestos/salud/skip', methods=['POST'])
def skip_health_video():
    global current_health, current_health_target  # Corregido el nombre de la variable
    current_health, current_health_target = new_ordered_health()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/health/{current_health}', _external=True), 'target': current_health_target})

# Boton salto familia
@app.route('/gestos/familia/skip', methods=['POST'])
def skip_family_video():
    global current_family, current_family_target  # Corregido el nombre de la variable
    current_family, current_family_target = new_ordered_family()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/family/{current_family}', _external=True), 'target': current_family_target})

# Boton salto comunicacion
@app.route('/gestos/comunicacion/skip', methods=['POST'])
def skip_comunication_video():
    global current_comunication, current_comunication_target  # Corregido el nombre de la variable
    current_comunication, current_comunication_target = new_ordered_comunication()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/comunication/{current_comunication}', _external=True), 'target': current_comunication_target})

# Boton salto tiempo
@app.route('/gestos/tiempo/skip', methods=['POST'])
def skip_time_video():
    global current_time, current_time_target  # Corregido el nombre de la variable
    current_time, current_time_target = new_ordered_time()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/time/{current_time}', _external=True), 'target': current_time_target})

# Boton salto verbos
@app.route('/gestos/verbos/skip', methods=['POST'])
def skip_verb_video():
    global current_verbs, current_verbs_target  # Corregido el nombre de la variable
    current_verbs, current_verbs_target = new_ordered_verbs()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/verbs/{current_verbs}', _external=True), 'target': current_verbs_target})

# Boton salto descripcion
@app.route('/gestos/descripcion/skip', methods=['POST'])
def skip_description_video():
    global current_description, current_description_target  # Corregido el nombre de la variable
    current_description, current_description_target = new_ordered_description()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/description/{current_description}', _external=True), 'target': current_description_target})

# Boton salto preguntas
@app.route('/gestos/preguntas/skip', methods=['POST'])
def skip_question_video():
    global current_question, current_question_target
    current_question, current_question_target = new_ordered_question()  # Corregido el nombre de la variable
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/questions/{current_question}', _external=True), 'target': current_question_target})

# Usar el modelo abecedario
@app.route('/gestos/predict', methods=['POST'])
def predict():
    return process_prediction(model, labels_dict)

# Usar el modelo saludos
@app.route('/gestos/saludos/predict', methods=['POST'])
def predict_saludos():
    return process_prediction(models, labels_dicts)  

# Usar el modelo emociones
@app.route('/gestos/emociones/predict', methods=['POST'])
def predict_emociones():
    return process_prediction(modelr, labels_dictr) 

# Usar el modelo presentacion
@app.route('/gestos/presentacion/predict', methods=['POST'])
def predict_presentation():
    return process_prediction(modelp, labels_dictp)  

# Usar el modelo negación
@app.route('/gestos/negacion/predict', methods=['POST'])
def predict_negation():
    return process_prediction(modeln, labels_dictn)

# Usar el modelo ubicación
@app.route('/gestos/ubicacion/predict', methods=['POST'])
def predict_location():
    return process_prediction(modelu_dict, labels_dictu)

# Usar el modelo problemas
@app.route('/gestos/problemas/predict', methods=['POST'])
def predict_problem():
    return process_prediction(modelps, labels_dictps)

# Usar el modelo estados de ánimo
@app.route('/gestos/estadosanimo/predict', methods=['POST'])
def predict_mood():
    return process_prediction(modeles, labels_dictes)

# Usar el modelo conducta
@app.route('/gestos/conducta/predict', methods=['POST'])
def predict_conduct():
    return process_prediction(modelc, labels_dictc)

# Usar el modelo salud
@app.route('/gestos/salud/predict', methods=['POST'])
def predict_health():
    return process_prediction(modelsb, labels_dictsb)

# Usar el modelo familia
@app.route('/gestos/familia/predict', methods=['POST'])
def predict_family():
    return process_prediction(modelf, labels_dictf)

# Usar el modelo comunicación
@app.route('/gestos/comunicacion/predict', methods=['POST'])
def predict_comunication():
    return process_prediction(modelcel, labels_dictcel)

# Usar el modelo tiempo
@app.route('/gestos/tiempo/predict', methods=['POST'])
def predict_time():
    return process_prediction(modelt, labels_dictt)

# Usar el modelo verbos
@app.route('/gestos/verbos/predict', methods=['POST'])
def predict_verbs():
    return process_prediction(modelv, labels_dictv)

# Usar el modelo descripcion
@app.route('/gestos/descripcion/predict', methods=['POST'])
def predict_description():
    return process_prediction(modeldc, labels_dictdc)

# Usar el modelo preguntas
@app.route('/gestos/preguntas/predict', methods=['POST'])
def predict_questions():
    return process_prediction(modelpe, labelspe_dict)

# Función para procesar la predicción
def process_prediction(model_used, labels):
    data = request.get_json()
    frame_base64 = data.get('frame')

    if not frame_base64:
        return jsonify({'prediction': 'No se recibió ningún frame'})
    try:
        frame_bytes = base64.b64decode(frame_base64)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            data_aux = []
            x_, y_ = [], []

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x, y = hand_landmarks.landmark[i].x, hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                if len(data_aux) > 42:
                    data_aux = data_aux[:42]
            
            prediction = model_used.predict([data_aux])
            predicted_index = int(prediction[0])
            predicted_character = labels.get(predicted_index, "Desconocido")
            
            # Determine if the prediction is correct based on the current target
            if labels == labels_dictr:
                is_correct = predicted_character.strip().lower() == current_emotion_target.strip().lower()
                return jsonify({'prediction': predicted_character, 'is_correct': is_correct, 'target': current_emotion_target})
            elif labels == labels_dictp:  # Añadido caso para presentación
                is_correct = predicted_character.strip().lower() == current_presentation_target.strip().lower()
                return jsonify({'prediction': predicted_character, 'is_correct': is_correct, 'target': current_presentation_target})
            else:
                is_correct = predicted_character.strip().lower() == current_target.strip().lower()
                return jsonify({'prediction': predicted_character, 'is_correct': is_correct, 'target': current_target})
        
        return jsonify({'prediction': 'No se detectó ninguna mano'})
    except Exception as e:
        return jsonify({'prediction': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5000)
