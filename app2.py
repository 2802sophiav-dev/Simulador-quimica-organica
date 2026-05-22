import random
import urllib.parse
import unicodedata
import streamlit.components.v1 as components
import streamlit as st

# ============================================
# VERIFICACIÓN DE RDKIT
# ============================================

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from rdkit.Chem import Draw

    RDKIT_DISPONIBLE = True

except ImportError:
    RDKIT_DISPONIBLE = False

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================

st.set_page_config(
    page_title="Simulador de Química Orgánica",
    page_icon="🧪",
    layout="wide"
)

# ============================================
# BARRA LATERAL
# ============================================

st.sidebar.title("Navegación del Módulo")
st.sidebar.markdown("---")

modulo = st.sidebar.radio(
    "Selecciona el nivel de la actividad:",
    [
        "Inicio",
        "Modulo I",
        "Modulo II",
        "Modulo III"
    ]
)

st.sidebar.markdown("---")

if modulo == "Inicio":

    st.title("🧪 Plataforma Interactiva de Química Orgánica")

    st.subheader(
        "Simulación, Termodinámica y Mecanismos de Reacción"
    )

    st.markdown("""
¡Bienvenido al entorno de evaluación y simulación!

Esta aplicación ha sido diseñada para integrar los conceptos
clave de Química Orgánica en un entorno web interactivo
utilizando Python y Streamlit.

###  Autores:

Creada por los estudiantes:

- **Sophia Vargas Vargas**
- **Juan Sebastian Peña Prado**
- **Juan Carlos Castillo Quitian**
- **Harold Santiago Alarcon Archila**

Estudiantes de **Ingeniería Química** de la
**Universidad Industrial de Santander (UIS)**.

---

### 📚 Estructura del entorno:

### 🔹 Modulo I
Nomenclatura de compuestos orgánicos y clasificación de reacciones.

### 🔹 Modulo II
Densidad electrónica y estabilidad
de intermedios de reacción.

### 🔹 Modulo III
Simulación cinética de reacciones
radicalarias y predicción de sitios de ataque.

---

Utiliza la barra lateral izquierda para navegar entre módulos.
""")
   

def ejecutar_modulo1():   

    # ============================================
    # NIVEL BAJO
    # ============================================


    st.title("📉 Modulo I: Nomenclatura y Reacciones.")

    st.write(
        "Completa las actividades para evaluar "
        "tus conocimientos."
    )

    st.markdown("---")

    # =========================================================
    # ACTIVIDAD 1: CONSTRUCTOR MOLECULAR
    # =========================================================

    st.header("Actividad 1: Constructor Molecular Interactivo")

    st.markdown(
        "Diseña estructuras orgánicas personalizadas y visualiza "
        "su geometría bidimensional en tiempo real."
    )

    # =========================================================
    # ESTADO DE SUSTITUYENTES
    # =========================================================

    if "susts" not in st.session_state:
        st.session_state.susts = []

    # =========================================================
    # TIPO DE ESTRUCTURA
    # =========================================================

    tipo = st.radio(
        "Tipo de estructura de soporte:",
        ["Cadena Abierta", "Cicloalcano"],
        key="constructor_tipo"
    )

    # =========================================================
    # NÚMERO DE CARBONOS
    # =========================================================

    num_carbonos = st.slider(
        "Número de carbonos principales:",
        3, 20, 5,
        key="constructor_slider"
    )

    # =========================================================
    # LISTA AMPLIADA DE GRUPOS
    # =========================================================

    grupos = [

        # HALÓGENOS
        "Flúor (-F)",
        "Cloro (-Cl)",
        "Bromo (-Br)",
        "Yodo (-I)",
        "Astato (-At)",
        "Teneso (-Ts)",

        # GRUPOS ALQUILO
        "Metil (-CH3)",
        "Etil (-C2H5)",
        "Propil (-C3H7)",
        "Isopropil",
        "Butil",
        "Isobutil",
        "Ter-butil",

        # FUNCIONES OXIGENADAS
        "Alcohol (-OH)",
        "Fenol",
        "Aldehído (-CHO)",
        "Cetona (>C=O)",
        "Ácido carboxílico (-COOH)",

        # FUNCIONES NITROGENADAS
        "Amina (-NH2)",
        "Amida (-CONH2)",
        "Nitrilo (-CN)",

        # EXTRA
        "Nitro (-NO2)"
    ]

    # =========================================================
    # SELECTORES
    # =========================================================

    col_c1, col_c2 = st.columns(2)

    with col_c1:

        grupo = st.selectbox(
            "Grupo funcional a añadir:",
            grupos,
            key="constructor_grupo"
        )

    with col_c2:

        posicion = st.number_input(
            "Posición del carbono (C-x):",
            1,
            num_carbonos,
            1,
            key="constructor_pos"
        )

    # =========================================================
    # BOTONES
    # =========================================================

    col_b1, col_b2 = st.columns(2)

    with col_b1:

        if st.button("➕ Agregar Grupo", key="btn_add_grupo"):

            st.session_state.susts.append({
                "grupo": grupo,
                "pos": posicion
            })

            st.success("Grupo agregado correctamente")
            st.rerun()

    with col_b2:

        if st.button("🗑️ Limpiar Estructura", key="btn_clean_mol"):

            st.session_state.susts = []

            st.success("Estructura reiniciada")
            st.rerun()

    # =========================================================
    # MOSTRAR GRUPOS AGREGADOS
    # =========================================================

    if st.session_state.susts:

        st.subheader("Sustituyentes agregados:")

        for s in st.session_state.susts:

            st.info(f"📍 C-{s['pos']} → {s['grupo']}")

    # =========================================================
    # VISUALIZACIÓN DE MOLÉCULA
    # =========================================================

    st.write("#### Vista Previa de la Estructura Química")

    if not RDKIT_DISPONIBLE:

        st.error(
            "⚠️ RDKit no está instalado correctamente."
        )

    else:

        try:

            mol = Chem.RWMol()

            atomos = {}

            # =====================================================
            # CREAR CADENA PRINCIPAL
            # =====================================================

            for i in range(1, num_carbonos + 1):

                idx = mol.AddAtom(Chem.Atom(6))

                atomos[i] = idx

            # =====================================================
            # ENLACES DE LA CADENA
            # =====================================================

            for i in range(1, num_carbonos):

                mol.AddBond(
                    atomos[i],
                    atomos[i + 1],
                    Chem.BondType.SINGLE
                )

            # =====================================================
            # CICLOALCANO
            # =====================================================

            if tipo == "Cicloalcano":

                mol.AddBond(
                    atomos[num_carbonos],
                    atomos[1],
                    Chem.BondType.SINGLE
                )

            # =====================================================
            # AGREGAR SUSTITUYENTES
            # =====================================================

            for s in st.session_state.susts:

                if s["pos"] <= num_carbonos:

                    parent = atomos[s["pos"]]

                    # =====================================================
                    # HALÓGENOS
                    # =====================================================

                    if s["grupo"] == "Flúor (-F)":

                        f = mol.AddAtom(Chem.Atom(9))
                        mol.AddBond(parent, f, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Cloro (-Cl)":

                        cl = mol.AddAtom(Chem.Atom(17))
                        mol.AddBond(parent, cl, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Bromo (-Br)":

                        br = mol.AddAtom(Chem.Atom(35))
                        mol.AddBond(parent, br, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Yodo (-I)":

                        i = mol.AddAtom(Chem.Atom(53))
                        mol.AddBond(parent, i, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Astato (-At)":

                        at = mol.AddAtom(Chem.Atom(85))
                        mol.AddBond(parent, at, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Teneso (-Ts)":

                        ts = mol.AddAtom(Chem.Atom(117))
                        mol.AddBond(parent, ts, Chem.BondType.SINGLE)

                    # =====================================================
                    # GRUPOS ALQUILO
                    # =====================================================

                    elif s["grupo"] == "Metil (-CH3)":

                        c = mol.AddAtom(Chem.Atom(6))
                        mol.AddBond(parent, c, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Etil (-C2H5)":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Propil (-C3H7)":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))
                        c3 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)
                        mol.AddBond(c2, c3, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Isopropil":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))
                        c3 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c3, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Butil":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))
                        c3 = mol.AddAtom(Chem.Atom(6))
                        c4 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)
                        mol.AddBond(c2, c3, Chem.BondType.SINGLE)
                        mol.AddBond(c3, c4, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Isobutil":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))
                        c3 = mol.AddAtom(Chem.Atom(6))
                        c4 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)
                        mol.AddBond(c2, c3, Chem.BondType.SINGLE)
                        mol.AddBond(c2, c4, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Ter-butil":

                        c1 = mol.AddAtom(Chem.Atom(6))
                        c2 = mol.AddAtom(Chem.Atom(6))
                        c3 = mol.AddAtom(Chem.Atom(6))
                        c4 = mol.AddAtom(Chem.Atom(6))

                        mol.AddBond(parent, c1, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c2, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c3, Chem.BondType.SINGLE)
                        mol.AddBond(c1, c4, Chem.BondType.SINGLE)

                    # =====================================================
                    # FUNCIONES OXIGENADAS
                    # =====================================================

                    elif s["grupo"] == "Alcohol (-OH)":

                        o = mol.AddAtom(Chem.Atom(8))
                        mol.AddBond(parent, o, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Fenol":

                        o = mol.AddAtom(Chem.Atom(8))
                        mol.AddBond(parent, o, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Aldehído (-CHO)":

                        o = mol.AddAtom(Chem.Atom(8))
                        mol.AddBond(parent, o, Chem.BondType.DOUBLE)

                    elif s["grupo"] == "Cetona (>C=O)":

                        o = mol.AddAtom(Chem.Atom(8))
                        mol.AddBond(parent, o, Chem.BondType.DOUBLE)

                    elif s["grupo"] == "Ácido carboxílico (-COOH)":

                        c = mol.AddAtom(Chem.Atom(6))
                        o1 = mol.AddAtom(Chem.Atom(8))
                        o2 = mol.AddAtom(Chem.Atom(8))

                        mol.AddBond(parent, c, Chem.BondType.SINGLE)
                        mol.AddBond(c, o1, Chem.BondType.DOUBLE)
                        mol.AddBond(c, o2, Chem.BondType.SINGLE)

                    # =====================================================
                    # FUNCIONES NITROGENADAS
                    # =====================================================

                    elif s["grupo"] == "Amina (-NH2)":

                        n = mol.AddAtom(Chem.Atom(7))
                        mol.AddBond(parent, n, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Amida (-CONH2)":

                        c = mol.AddAtom(Chem.Atom(6))
                        o = mol.AddAtom(Chem.Atom(8))
                        n = mol.AddAtom(Chem.Atom(7))

                        mol.AddBond(parent, c, Chem.BondType.SINGLE)
                        mol.AddBond(c, o, Chem.BondType.DOUBLE)
                        mol.AddBond(c, n, Chem.BondType.SINGLE)

                    elif s["grupo"] == "Nitrilo (-CN)":

                        c = mol.AddAtom(Chem.Atom(6))
                        n = mol.AddAtom(Chem.Atom(7))

                        mol.AddBond(parent, c, Chem.BondType.SINGLE)
                        mol.AddBond(c, n, Chem.BondType.TRIPLE)

                    # =====================================================
                    # NITRO
                    # =====================================================

                    elif s["grupo"] == "Nitro (-NO2)":

                        n = mol.AddAtom(Chem.Atom(7))
                        o1 = mol.AddAtom(Chem.Atom(8))
                        o2 = mol.AddAtom(Chem.Atom(8))

                        mol.AddBond(parent, n, Chem.BondType.SINGLE)
                        mol.AddBond(n, o1, Chem.BondType.DOUBLE)
                        mol.AddBond(n, o2, Chem.BondType.SINGLE)

            # =====================================================
            # GENERAR MOLÉCULA
            # =====================================================

            display_mol = mol.GetMol()

            try:

                Chem.SanitizeMol(display_mol)

            except Exception as e:

                st.warning(f"Advertencia estructural: {e}")

            # =====================================================
            # COORDENADAS 2D
            # =====================================================

            AllChem.Compute2DCoords(display_mol)

            # =====================================================
            # IMAGEN
            # =====================================================

            imagen_final = Draw.MolToImage(
                display_mol,
                size=(700, 400)
            )

            st.image(
                imagen_final,
                caption="Estructura Molecular"
            )

            # =====================================================
            # SMILES
            # =====================================================

            smiles = Chem.MolToSmiles(display_mol)

            st.code(smiles, language="text")

        except Exception as e:

            st.error(
                f"❌ Error al generar la molécula: {e}"
            )

    # =========================================================
    # VALIDAR NOMENCLATURA DEL COMPUESTO
    # =========================================================

    st.header("🧪 Verificación de Nomenclatura")

    st.write(
        "Escribe el nombre del compuesto que construiste."
    )

    # =========================================================
    # FUNCIÓN PARA NORMALIZAR TEXTO
    # =========================================================

    def normalizar_texto(texto):

        texto = texto.lower().strip()

        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

        texto = " ".join(texto.split())

        return texto

    # =========================================================
    # GENERAR NOMBRE ESPERADO
    # =========================================================

    def prefijo_carbonos(n):

        prefijos = {
            1: "met",
            2: "et",
            3: "prop",
            4: "but",
            5: "pent",
            6: "hex",
            7: "hept",
            8: "oct"
        }

        return prefijos.get(n, "")

    sustituyentes_dict = {

        "Flúor (-F)": "fluoro",
        "Cloro (-Cl)": "cloro",
        "Bromo (-Br)": "bromo",
        "Yodo (-I)": "yodo",
        "Astato (-At)": "astato",
        "Teneso (-Ts)": "teneso",

        "Metil (-CH3)": "metil",
        "Etil (-C2H5)": "etil",
        "Propil (-C3H7)": "propil",
        "Isopropil": "isopropil",
        "Butil": "butil",
        "Isobutil": "isobutil",
        "Ter-butil": "ter-butil",

        "Nitro (-NO2)": "nitro"
    }

    # =========================================================
    # FUNCIÓN PRINCIPAL DE NOMENCLATURA IUPAC
    # =========================================================

    def generar_nombre():

        base = prefijo_carbonos(num_carbonos)

        # =====================================================
        # NOMBRE BASE
        # =====================================================

        if tipo == "Cadena Abierta":
            nombre_base = base + "ano"
        else:
            nombre_base = "ciclo" + base + "ano"

        # =====================================================
        # PRIORIDADES IUPAC
        # =====================================================

        prioridades = {
            "Ácido carboxílico (-COOH)": 1,
            "Amida (-CONH2)": 2,
            "Nitrilo (-CN)": 3,
            "Aldehído (-CHO)": 4,
            "Cetona (>C=O)": 5,
            "Alcohol (-OH)": 6,
            "Amina (-NH2)": 7,
            "Fenol": 8
        }

        # =====================================================
        # SUFIJOS IUPAC
        # =====================================================

        sufijos = {
            "Ácido carboxílico (-COOH)": "oico",
            "Amida (-CONH2)": "amida",
            "Nitrilo (-CN)": "nitrilo",
            "Aldehído (-CHO)": "al",
            "Cetona (>C=O)": "ona",
            "Alcohol (-OH)": "ol",
            "Amina (-NH2)": "amina",
            "Fenol": "fenol"
        }

        # =====================================================
        # PREFIJOS CUANDO NO SON PRINCIPALES
        # =====================================================

        prefijos_funcionales = {
            "Cetona (>C=O)": "oxo",
            "Alcohol (-OH)": "hidroxi",
            "Amina (-NH2)": "amino",
            "Aldehído (-CHO)": "formil",
            "Ácido carboxílico (-COOH)": "carboxi",
            "Amida (-CONH2)": "carbamoil",
            "Nitrilo (-CN)": "ciano",
            "Fenol": "hidroxi"
        }

        # =====================================================
        # SUSTITUYENTES NORMALES
        # =====================================================

        prefijos_simples = []

        # =====================================================
        # GRUPOS FUNCIONALES
        # =====================================================

        grupos_funcionales = []

        for s in st.session_state.susts:

            grupo = s["grupo"]
            pos = s["pos"]

            if grupo in prioridades:

                grupos_funcionales.append({
                    "grupo": grupo,
                    "pos": pos,
                    "prioridad": prioridades[grupo]
                })

            elif grupo in sustituyentes_dict:

                prefijos_simples.append(
                    f"{pos}-{sustituyentes_dict[grupo]}"
                )

        # =====================================================
        # DETERMINAR FUNCIÓN PRINCIPAL
        # =====================================================

        funcion_principal = None

        if grupos_funcionales:

            funcion_principal = min(
                grupos_funcionales,
                key=lambda x: x["prioridad"]
            )

        # =====================================================
        # PREFIJOS EXTRA
        # =====================================================

        prefijos_extra = []

        for gf in grupos_funcionales:

            grupo = gf["grupo"]
            pos = gf["pos"]

            # Saltar función principal
            if funcion_principal and gf == funcion_principal:
                continue

            # Convertir a prefijo
            prefijo = prefijos_funcionales.get(grupo)

            if prefijo:

                prefijos_extra.append(
                    f"{pos}-{prefijo}"
                )

        # =====================================================
        # ORDENAR PREFIJOS
        # =====================================================

        todos_prefijos = prefijos_simples + prefijos_extra
        todos_prefijos.sort()

        # =====================================================
        # GENERAR SUFIJO PRINCIPAL
        # =====================================================

        if funcion_principal:

            grupo = funcion_principal["grupo"]
            pos = funcion_principal["pos"]

            sufijo = sufijos[grupo]

            # ================================================
            # ÁCIDO
            # ================================================

            if sufijo == "oico":

                nombre_base = f"ácido {base}anoico"

            # ================================================
            # ALDEHÍDO
            # ================================================

            elif sufijo == "al":

                nombre_base = f"{base}anal"

            # ================================================
            # CETONA
            # ================================================

            elif sufijo == "ona":

                nombre_base = (
                    f"{base}an-{pos}-ona"
                )

            # ================================================
            # ALCOHOL
            # ================================================

            elif sufijo == "ol":

                nombre_base = (
                    f"{base}an-{pos}-ol"
                )

            # ================================================
            # AMINA
            # ================================================

            elif sufijo == "amina":

                nombre_base = (
                    f"{base}an-{pos}-amina"
                )

            # ================================================
            # AMIDA
            # ================================================

            elif sufijo == "amida":

                nombre_base = (
                    f"{base}anamida"
                )

            # ================================================
            # NITRILO
            # ================================================

            elif sufijo == "nitrilo":

                nombre_base = (
                    f"{base}anonitrilo"
                )

            # ================================================
            # FENOL
            # ================================================

            elif sufijo == "fenol":

                nombre_base = "fenol"

        # =====================================================
        # UNIR TODO
        # =====================================================

        if todos_prefijos:

            nombre_final = (
                "-".join(todos_prefijos)
                + " "
                + nombre_base
            )

        else:

            nombre_final = nombre_base

        return nombre_final

    # =========================================================
    # RESPUESTA DEL USUARIO
    # =========================================================

    nombre_usuario = st.text_input(
        "Nombre del compuesto:",
        key="nombre_usuario"
    )

    nombre_correcto = generar_nombre()

    # =========================================================
    # BOTÓN DE VERIFICACIÓN
    # =========================================================

    if st.button("✅ Verificar Nombre"):

        if nombre_usuario.strip() == "":

            st.warning(
                "⚠️ Debes escribir un nombre."
            )

        else:

            respuesta_usuario = normalizar_texto(nombre_usuario)
            respuesta_correcta = normalizar_texto(nombre_correcto)

            if respuesta_usuario == respuesta_correcta:

                st.success(
                    "🎉 ¡Correcto! La nomenclatura está bien escrita."
                )

                st.balloons()

            else:

                st.error(
                    "❌ La nomenclatura es incorrecta."
                )

                st.warning(
                    "🔁 Inténtalo nuevamente."
                )

                st.info(
                    "💡 Revisa posiciones, prefijos y sufijos."
                )

    # =========================================================
    # MOSTRAR RESPUESTA CORRECTA
    # =========================================================

    with st.expander("🔍 Ver respuesta correcta"):

        st.write(nombre_correcto)

    # =========================================================
    # ACTIVIDAD 2
    # =========================================================

    st.header("Actividad 2: Clasificación de Reacciones")

    st.markdown(
        "Analiza la reacción química y clasifica "
        "el tipo de reacción."
    )

    reacciones_pool = [

        {
            "latex":
            r"CH_4 + Cl_2 \xrightarrow{h\nu} CH_3Cl + HCl",

            "correct":
            "Sustitución",

            "success_msg":
            "🎉 Correcto. Es una sustitución radicalaria.",

            "error_msg":
            "❌ Incorrecto. El Cl reemplaza un H."
        },

        {
            "latex":
            r"CH_2=CH_2 + H_2 \xrightarrow{Pt} CH_3-CH_3",

            "correct":
            "Adición",

            "success_msg":
            "🎉 Correcto. Los H se adicionan al doble enlace.",

            "error_msg":
            "❌ Incorrecto. Se rompe una insaturación."
        },

        {
            "latex":
            r"CH_3-CH_2OH \xrightarrow{H_2SO_4, \Delta} CH_2=CH_2 + H_2O",

            "correct":
            "Eliminación",

            "success_msg":
            "🎉 Correcto. Se forma un doble enlace.",

            "error_msg":
            "❌ Incorrecto. Se eliminan átomos."
        },

        {
            "latex":
            r"CH_2=CH_2 + Br_2 \rightarrow CH_2Br-CH_2Br",

            "correct":
            "Adición",

            "success_msg":
            "🎉 Correcto. El Br₂ se adiciona al doble enlace.",

            "error_msg":
            "❌ Incorrecto. La reacción rompe el doble enlace."
        },

        {
            "latex":
            r"CH_3-CH_2Br + OH^- \rightarrow CH_3-CH_2OH + Br^-",

            "correct":
            "Sustitución",

            "success_msg":
            "🎉 Correcto. El OH reemplaza al Br.",

            "error_msg":
            "❌ Incorrecto. Hay reemplazo de grupos."
        },

        {
            "latex":
            r"CH_3-CHBr-CH_3 \xrightarrow{KOH} CH_3-CH=CH_2 + HBr",

            "correct":
            "Eliminación",

            "success_msg":
            "🎉 Correcto. Se elimina HBr y aparece un doble enlace.",

            "error_msg":
            "❌ Incorrecto. Se pierden átomos."
        },

        {
            "latex":
            r"CH_3-CH=CH_2 + HCl \rightarrow CH_3-CHCl-CH_3",

            "correct":
            "Adición",

            "success_msg":
            "🎉 Correcto. HCl se adiciona al doble enlace.",

            "error_msg":
            "❌ Incorrecto. La insaturación desaparece."
        },

        {
            "latex":
            r"C_6H_6 + Br_2 \xrightarrow{FeBr_3} C_6H_5Br + HBr",

            "correct":
            "Sustitución",

            "success_msg":
            "🎉 Correcto. Un H del benceno es reemplazado.",

            "error_msg":
            "❌ Incorrecto. Hay sustitución aromática."
        },

        {
            "latex":
            r"CH_3-CH_2-CH_2OH \xrightarrow{\Delta} CH_3-CH=CH_2 + H_2O",

            "correct":
            "Eliminación",

            "success_msg":
            "🎉 Correcto. Se elimina agua y se forma un alqueno.",

            "error_msg":
            "❌ Incorrecto. La reacción genera una insaturación."
        },

        {
            "latex":
            r"CH_3-CH=CH_2 + H_2O \xrightarrow{H^+} CH_3-CHOH-CH_3",

            "correct":
            "Adición",

            "success_msg":
            "🎉 Correcto. El agua se adiciona al doble enlace.",

            "error_msg":
            "❌ Incorrecto. Es una hidratación."
        }
    ]

    # =========================================================
    # INICIALIZAR REACCIÓN
    # =========================================================

    if "reaccion_seleccionada" not in st.session_state:

        st.session_state.reaccion_seleccionada = random.choice(
            reacciones_pool
        )

    reaccion_actual = st.session_state.reaccion_seleccionada

    # =========================================================
    # MOSTRAR REACCIÓN
    # =========================================================

    st.latex(reaccion_actual["latex"])

    # =========================================================
    # OPCIONES
    # =========================================================

    opciones_reaccion = [

        "Selecciona una opción",

        "Adición (Suma de reactivos sobre un enlace insaturado)",

        "Eliminación (Pérdida de átomos para formar una insaturación)",

        "Sustitución (Un átomo o grupo reemplaza a otro)",

        "Rearreglo (Isomerización sin pérdida de átomos)"
    ]

    opcion_reaccion = st.radio(
        "Selecciona el tipo de reacción correcto:",
        opciones_reaccion,
        key="radio_a2"
    )

    # =========================================================
    # BOTONES
    # =========================================================

    col_btn_a2_1, col_btn_a2_2 = st.columns([1, 4])

    with col_btn_a2_1:

        validar_a2 = st.button(
            "Validar Actividad 2"
        )

    with col_btn_a2_2:

        if st.button(
            "🔄 Cambiar reacción",
            key="btn_cambiar_a2"
        ):

            st.session_state.reaccion_seleccionada = random.choice(
                reacciones_pool
            )

            st.rerun()

    # =========================================================
    # VALIDACIÓN
    # =========================================================

    if validar_a2:

        if opcion_reaccion == "Selecciona una opción":

            st.warning(
                "⚠️ Debes seleccionar una opción."
            )

        elif reaccion_actual["correct"] in opcion_reaccion:

            st.success(
                reaccion_actual["success_msg"]
            )

            st.balloons()

        else:

            st.error(
                reaccion_actual["error_msg"]
            )

    st.markdown("---")


# ============================================
# NIVEL MEDIO: Reactividad y Estabilidad
# ============================================


def ejecutar_modulo2():


    # Limpieza de estados
    for key in [
        "compuesto_seleccionado",
        "reaccion_seleccionada",
        "radical_seleccionado"
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.title("⚙️ Modulo II: Reactividad y Estabilidad")

    st.markdown("""
    En esta sección evaluaremos tu capacidad para predecir
    el comportamiento de las moléculas basándote en la
    distribución electrónica y la estabilidad de intermedios.
    """)

    tabs = st.tabs([
        "🎯 Densidad Electrónica",
        "⚖️ Estabilidad de Intermedios"
    ])

    # =========================================================
    # TAB 1: DENSIDAD ELECTRÓNICA
    # =========================================================

    with tabs[0]:

        st.header("Mapeo de Centros Reactivos")

        st.write(
            "Identifica si el centro marcado actúa como "
            "Nucleófilo o Electrófilo."
        )

        ejercicios_densidad = [

            {
                "molecula": "CH3 — Br",
                "centro": "Carbono unido al Bromo",
                "tipo": "Electrófilo (δ+)",
                "justificacion":
                "El Bromo es más electronegativo y retira densidad electrónica."
            },

            {
                "molecula": "CH3 — NH2",
                "centro": "Nitrógeno (Par solitario)",
                "tipo": "Nucleófilo (δ-)",
                "justificacion":
                "El Nitrógeno posee un par libre capaz de donar electrones."
            },

            {
                "molecula": "CH3 — C(=O) — CH3",
                "centro": "Carbono del Carbonilo",
                "tipo": "Electrófilo (δ+)",
                "justificacion":
                "El Oxígeno atrae electrones dejando parcialmente positivo al Carbono."
            },

            {
                "molecula": "CH3 — OH",
                "centro": "Oxígeno",
                "tipo": "Nucleófilo (δ-)",
                "justificacion":
                "El Oxígeno tiene pares libres que puede donar."
            },

            {
                "molecula": "H — Cl",
                "centro": "Hidrógeno",
                "tipo": "Electrófilo (δ+)",
                "justificacion":
                "El Cloro atrae electrones y deja al Hidrógeno parcialmente positivo."
            },

            {
                "molecula": "NH3",
                "centro": "Nitrógeno",
                "tipo": "Nucleófilo (δ-)",
                "justificacion":
                "El amoníaco tiene un par libre disponible para reaccionar."
            },

            {
                "molecula": "CH3 — Li",
                "centro": "Carbono unido al Litio",
                "tipo": "Nucleófilo (δ-)",
                "justificacion":
                "El Litio es poco electronegativo y el Carbono gana densidad electrónica."
            },

            {
                "molecula": "SO3",
                "centro": "Azufre",
                "tipo": "Electrófilo (δ+)",
                "justificacion":
                "Los Oxígenos atraen electrones dejando deficiente al Azufre."
            },

            {
                "molecula": "CN⁻",
                "centro": "Carbono del Cianuro",
                "tipo": "Nucleófilo (δ-)",
                "justificacion":
                "El ion cianuro posee alta densidad electrónica."
            },

            {
                "molecula": "BF3",
                "centro": "Boro",
                "tipo": "Electrófilo (δ+)",
                "justificacion":
                "El Boro tiene un octeto incompleto y acepta electrones."
            }
        ]

        # Estado inicial
        if "idx_densidad" not in st.session_state:
            st.session_state.idx_densidad = 0

        ejercicio_actual = ejercicios_densidad[
            st.session_state.idx_densidad
        ]

        st.info(
            f"**Molécula:** {ejercicio_actual['molecula']}"
        )

        st.warning(
            f"**Centro a analizar:** "
            f"{ejercicio_actual['centro']}"
        )

        opcion_densidad = st.radio(
            "¿Cómo se comporta este centro?",
            [
                "Selecciona una opción",
                "Nucleófilo (δ-)",
                "Electrófilo (δ+)"
            ],
            key=f"densidad_{st.session_state.idx_densidad}"
        )

        if st.button("Validar Centro"):

            if ejercicio_actual["tipo"] == opcion_densidad:

                st.success(
                    f"✅ ¡Correcto! "
                    f"{ejercicio_actual['justificacion']}"
                )

            else:

                st.error(
                    "❌ Incorrecto. "
                    "Revisa la electronegatividad y "
                    "la distribución electrónica."
                )

        if st.button("Siguiente Molécula ➡️"):

            st.session_state.idx_densidad = (
                st.session_state.idx_densidad + 1
            ) % len(ejercicios_densidad)

            st.rerun()

    # =========================================================
    # TAB 2: ESTABILIDAD DE INTERMEDIOS
    # =========================================================

    with tabs[1]:

        st.header("Estabilidad de Intermedios")

        st.write(
            "Ordena los intermedios de "
            "**Menor (1) a Mayor (3) estabilidad**."
        )

        ejercicios_intermedios = [

            {
                "titulo": "Carbocationes",
                "moleculas": [
                    ("R — CH2(+)", 1),
                    ("R — CH(+) — R", 2),
                    ("R — C(+)(R) — R", 3),
                ],
                "explicacion":
                "Los grupos alquilo estabilizan la carga positiva por efecto inductivo."
            },

            {
                "titulo": "Radicales Libres",
                "moleculas": [
                    ("CH3•", 1),
                    ("R — CH• — R", 2),
                    ("R3C•", 3),
                ],
                "explicacion":
                "Los radicales terciarios son más estables por hiperconjugación."
            },

            {
                "titulo": "Carbaniones",
                "moleculas": [
                    ("R3C⁻", 1),
                    ("R2CH⁻", 2),
                    ("RCH2⁻", 3),
                ],
                "explicacion":
                "Los grupos alquilo desestabilizan la carga negativa."
            },

            {
                "titulo": "Carbocationes Resonantes",
                "moleculas": [
                    ("CH3⁺", 1),
                    ("Carbocatión secundario", 2),
                    ("Carbocatión alílico", 3),
                ],
                "explicacion":
                "La resonancia proporciona gran estabilidad."
            },

            {
                "titulo": "Radicales Resonantes",
                "moleculas": [
                    ("CH3•", 1),
                    ("Radical secundario", 2),
                    ("Radical bencílico", 3),
                ],
                "explicacion":
                "Los radicales bencílicos se estabilizan por resonancia."
            }
        ]

        # Estado inicial
        if "idx_intermedio" not in st.session_state:
            st.session_state.idx_intermedio = 0

        ejercicio_int = ejercicios_intermedios[
            st.session_state.idx_intermedio
        ]

        shuffle_key = f"shuffle_{st.session_state.idx_intermedio}"

        if shuffle_key not in st.session_state:

            moleculas_mezcladas = ejercicio_int["moleculas"].copy()
            random.shuffle(moleculas_mezcladas)

            st.session_state[shuffle_key] = moleculas_mezcladas

        moleculas = st.session_state[shuffle_key]

        st.subheader(
            f"Ejercicio: {ejercicio_int['titulo']}"
        )

        col1, col2, col3 = st.columns(3)

        rankings = []

        for i, (col, mol_data) in enumerate(
            zip([col1, col2, col3], moleculas)
        ):

            molecula, valor_correcto = mol_data

            with col:

                st.code(molecula, language="text")

                rank = st.number_input(
                    "Rango",
                    min_value=1,
                    max_value=3,
                    key=f"rank_{st.session_state.idx_intermedio}_{i}"
                )

                rankings.append((rank, valor_correcto))

        # =========================================================
        # COMPROBAR RESPUESTA
        # =========================================================

        if st.button("Comprobar Ordenamiento"):

            rangos_usuario = [x[0] for x in rankings]
            valores_correctos = [x[1] for x in rankings]

            if len(set(rangos_usuario)) < 3:

                st.warning(
                    "⚠️ No puedes repetir rangos."
                )

            elif rangos_usuario == valores_correctos:

                st.success(
                    f"✅ ¡Correcto!\n\n"
                    f"{ejercicio_int['explicacion']}"
                )

                st.balloons()

            else:

                st.error(
                    "❌ El ordenamiento es incorrecto."
                )

        # =========================================================
        # SIGUIENTE EJERCICIO
        # =========================================================

        if st.button("Siguiente Ejercicio ➡️"):

            st.session_state.idx_intermedio = (
                st.session_state.idx_intermedio + 1
            ) % len(ejercicios_intermedios)

            st.rerun()


def ejecutar_modulo3():
        
    # Indent everything inside the function by 4 spaces
    from rdkit import Chem
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D

    # =========================================================
    # CONFIGURACIÓN GENERAL
    # =========================================================
    st.title("📉 Modulo III: Simulador de Mecanismos Organicos.")
    # =========================================================
    # ESTADO DE SESIÓN
    # =========================================================
    if "paso" not in st.session_state:
        st.session_state.paso = 0

    if "reaccion" not in st.session_state:
        st.session_state.reaccion = None

    if "sustrato_nombre" not in st.session_state:
        st.session_state.sustrato_nombre = None

    if "historial" not in st.session_state:
        st.session_state.historial = []

    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

    # =========================================================
    # FUNCIÓN DE DIBUJO SVG MEJORADA
    # =========================================================
    def dibujar_molecula(smiles, titulo, flecha=None):
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                st.error(f"No se pudo interpretar el SMILES:\n{smiles}")
                return

            # -------------------------------------------------
            # GENERAR COORDENADAS 2D
            # -------------------------------------------------
            rdDepictor.Compute2DCoords(mol)

            # -------------------------------------------------
            # SVG MÁS GRANDE
            # -------------------------------------------------
            width = 700
            height = 400
            drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
            opts = drawer.drawOptions()

            # ==========================================
            # AJUSTES IMPORTANTES
            # ==========================================
            opts.padding = 0.15 
            opts.centreMoleculesBeforeDrawing = True 
            opts.bondLineWidth = 2.8 
            opts.baseFontSize = 1.0
            opts.maxFontSize = 28
            opts.minFontSize = 16 
            opts.additionalAtomLabelPadding = 0.25
            Chem.rdDepictor.SetPreferCoordGen(True)
            opts.clearBackground = False 
            opts.explicitMethyl = True

            # -------------------------------------------------
            # DIBUJAR MOLÉCULA
            # -------------------------------------------------
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()
            svg = drawer.GetDrawingText()

            # -------------------------------------------------
            # LIMPIEZA SVG
            # -------------------------------------------------
            svg = svg.replace("svg:", "")

            # =================================================
            # FLECHAS CURVAS
            # =================================================
            arrow_svg = ""
            if flecha:
                # Escalamos un poco las coordenadas viejas a la nueva proporción si es necesario
                x1, y1 = flecha["coords_inicio"][0] * 0.75, flecha["coords_inicio"][1] * 0.6
                x2, y2 = flecha["coords_fin"][0] * 0.75, flecha["coords_fin"][1] * 0.6
                cx = (x1 + x2) / 2
                cy = min(y1, y2) - 40
                arrow_svg = f"""
                <svg width="100%" height="100%" viewBox="0 0 {width} {height}" style="position:absolute; top:0; left:0; pointer-events:none; overflow:visible;">
                    <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                            <polygon points="0 0, 10 5, 0 10" fill="#d10000"/>
                        </marker>
                    </defs>
                    <path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" stroke="#d10000" stroke-width="3" stroke-linecap="round" marker-end="url(#arrowhead)" />
                </svg>
                """

            # =================================================
            # HTML FINAL
            # =================================================
            html = f"""
            <div style="position:relative; width:100%; max-width:{width}px; height:{height}px; margin:auto; border-radius:12px; background:white; overflow:hidden; display:flex; justify-content:center; align-items:center;">
                <div style="width:100%; height:100%;">
                    {svg}
                </div>
                {arrow_svg}
            </div>
            """
            st.markdown(f"#### {titulo}")
            #components.html(
                #html,
                #height=height + 10,
                #scrolling=False
            #)
            st.write("Visualización molecular cargada")
            st.image(img, use_column_width=True)
            
        except Exception as e:
            st.error(f"Error al dibujar:\n{e}")

    # =========================================================
    # SMILES INICIALES
    # =========================================================
    SMILES_INICIALES = {
        "Acetaldehído (Etanal)": "CC=O",
        "Propanal": "CCC=O",
        "Acetona (Propanona)": "CC(=O)C",
        "Butanona": "CCC(=O)C",
        "Ciclohexanona": "O=C1CCCCC1"
    }

    # =========================================================
    # BASE DE MECANISMOS
    # =========================================================
    BASE_MECANISMOS = {

        # =====================================================
        # IMINAS
        # =====================================================
        "Iminas (Aminas 1°)": {

            # =================================================
            # ACETONA
            # =================================================
            "Acetona (Propanona)": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CC([O-])([NH2+]C)C",
                    "explicacion": "La amina primaria ataca al carbono del carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 2: Transferencia de protón",
                    "origen_correcto": "Par libre del Oxígeno (Alkóxido)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CC(O)(NC)C",
                    "explicacion": "Formación de la carbinolamina.",
                    "imagen_concepto": "Carbinolamina",
                    "flecha": {
                        "coords_inicio": [360, 180],
                        "coords_fin": [260, 240]
                    }
                },
                {
                    "titulo": "Paso 3: Protonación del grupo OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CC([OH2+])(NC)C",
                    "explicacion": "El grupo OH se protona.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 4: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CC(=[NH+]C)C",
                    "explicacion": "El nitrógeno forma el doble enlace y sale agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 5: Formación de la imina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CC(=NC)C",
                    "explicacion": "Desprotonación final.",
                    "imagen_concepto": "Imina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ],

            # =================================================
            # ACETALDEHÍDO
            # =================================================
            "Acetaldehído (Etanal)": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CC([O-])[NH2+]C",
                    "explicacion": "La amina ataca al carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [340, 210]
                    }
                },
                {
                    "titulo": "Paso 2: Transferencia de protón",
                    "origen_correcto": "Par libre del Oxígeno (Alkóxido)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CC(O)NC",
                    "explicacion": "Carbinolamina.",
                    "imagen_concepto": "Carbinolamina",
                    "flecha": {
                        "coords_inicio": [340, 170],
                        "coords_fin": [250, 240]
                    }
                },
                {
                    "titulo": "Paso 3: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CC([OH2+])NC",
                    "explicacion": "OH protonado.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [340, 170],
                        "coords_fin": [420, 120]
                    }
                },
                {
                    "titulo": "Paso 4: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CC=[NH+]C",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 250],
                        "coords_fin": [340, 210]
                    }
                },
                {
                    "titulo": "Paso 5: Formación de la imina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CC=NC",
                    "explicacion": "Imina final.",
                    "imagen_concepto": "Imina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [350, 250]
                    }
                }
            ],

            # =================================================
            # BUTANONA
            # =================================================
            "Butanona": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CCC([O-])([NH2+]C)C",
                    "explicacion": "Ataque nucleofílico.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [360, 210]
                    }
                },
                {
                    "titulo": "Paso 2: Transferencia de protón",
                    "origen_correcto": "Par libre del Oxígeno (Alkóxido)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CCC(O)(NC)C",
                    "explicacion": "Formación de carbinolamina.",
                    "imagen_concepto": "Carbinolamina",
                    "flecha": {
                        "coords_inicio": [360, 170],
                        "coords_fin": [260, 240]
                    }
                },
                {
                    "titulo": "Paso 3: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CCC([OH2+])(NC)C",
                    "explicacion": "Protonación del OH.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 4: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CCC(=[NH+]C)C",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 5: Formación de la imina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CCC(=NC)C",
                    "explicacion": "Imina final.",
                    "imagen_concepto": "Imina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ],

            # =================================================
            # PROPANAL
            # =================================================
            "Propanal": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CCC([O-])[NH2+]C",
                    "explicacion": "La amina ataca al carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 2: Transferencia de protón",
                    "origen_correcto": "Par libre del Oxígeno (Alkóxido)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CCC(O)NC",
                    "explicacion": "Formación de carbinolamina.",
                    "imagen_concepto": "Carbinolamina",
                    "flecha": {
                        "coords_inicio": [360, 180],
                        "coords_fin": [260, 240]
                    }
                },
                {
                    "titulo": "Paso 3: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CCC([OH2+])NC",
                    "explicacion": "El OH se protona.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 4: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CCC=[NH+]C",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 5: Formación de la imina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "CCC=NC",
                    "explicacion": "Desprotonación final.",
                    "imagen_concepto": "Imina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ],

            # =================================================
            # CICLOHEXANONA
            # =================================================
            "Ciclohexanona": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "C1CCC([O-])([NH2+]C)CC1",
                    "explicacion": "Ataque nucleofílico al carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [250, 270],
                        "coords_fin": [350, 210]
                    }
                },
                {
                    "titulo": "Paso 2: Transferencia de protón",
                    "origen_correcto": "Par libre del Oxígeno (Alkóxido)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "C1CCC(O)(NC)CC1",
                    "explicacion": "Neutralización.",
                    "imagen_concepto": "Carbinolamina",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [250, 250]
                    }
                },
                {
                    "titulo": "Paso 3: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "C1CCC([OH2+])(NC)CC1",
                    "explicacion": "El OH se protona.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 4: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "C1CCC(=[NH+]C)CC1",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [350, 210]
                    }
                },
                {
                    "titulo": "Paso 5: Formación de la imina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón unido al Nitrógeno (H+)",
                    "smiles_resultado": "C1CCC(=NC)CC1",
                    "explicacion": "Desprotonación final.",
                    "imagen_concepto": "Imina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ]
        },

        # =====================================================
        # ENAMINAS
        # =====================================================
        "Enaminas (Aminas 2°)": {

            # =================================================
            # ACETALDEHÍDO - ¡NUEVO COMPUESTO AGREGADO!
            # =================================================
            "Acetaldehído (Etanal)": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CC([O-])[N+](C)C",
                    "explicacion": "La amina secundaria ataca al carbonilo del acetaldehído.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [340, 210]
                    }
                },
                {
                    "titulo": "Paso 2: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CC([OH2+])N(C)C",
                    "explicacion": "El grupo hidroxilo de la carbinolamina se protona para convertirse en un buen grupo saliente (agua).",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [340, 170],
                        "coords_fin": [420, 120]
                    }
                },
                {
                    "titulo": "Paso 3: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "C=C[NH+](C)C",
                    "explicacion": "El par libre del nitrógeno empuja para expulsar la molécula de agua, formando el doble enlace C=N+.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 250],
                        "coords_fin": [340, 210]
                    }
                },
                {
                    "titulo": "Paso 4: Formación de la enamina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón del Carbono Alfa (C-H)",
                    "smiles_resultado": "C=CN(C)C",
                    "explicacion": "El agua remueve un protón del carbono alfa, los electrones migran para formar el doble enlace C=C y neutralizan la carga del nitrógeno.",
                    "imagen_concepto": "Enamina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [350, 250]
                    }
                }
            ],

            # =================================================
            # ACETONA
            # =================================================
            "Acetona (Propanona)": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CC([O-])([N+](C)C)C",
                    "explicacion": "La amina secundaria ataca al carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 2: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CC([OH2+])(N(C)C)C",
                    "explicacion": "El OH se protona.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 3: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CC(=[N+](C)C)C",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 4: Formación de la enamina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón del Carbono Alfa (C-H)",
                    "smiles_resultado": "CC(=C)N(C)C",
                    "explicacion": "Desprotonación alfa.",
                    "imagen_concepto": "Enamina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [350, 250]
                    }
                }
            ],

            # =================================================
            # BUTANONA
            # =================================================
            "Butanona": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CCC([O-])([N+](C)C)C",
                    "explicacion": "Ataque nucleofílico.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 2: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CCC([OH2+])(N(C)C)C",
                    "explicacion": "OH protonado.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 3: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CCC(=[N+](C)C)C",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 250],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 4: Formación de la enamina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón del Carbono Alfa (C-H)",
                    "smiles_resultado": "CCC(=C)N(C)C",
                    "explicacion": "Formación de enamina.",
                    "imagen_concepto": "Enamina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ],

            # =================================================
            # PROPANAL - ¡NUEVO COMPUESTO AGREGADO!
            # =================================================
            "Propanal": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "CCC([O-])[N+](C)C",
                    "explicacion": "La amina secundaria efectúa el ataque nucleofílico sobre el propanal.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 2: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "CCC([OH2+])N(C)C",
                    "explicacion": "El oxígeno capta un protón del medio ácido facilitando la posterior eliminación.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 3: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "CC=C[NH+](C)C",
                    "explicacion": "Se asiste la salida del agua mediante la formación del doble enlace C=N+ por parte del nitrógeno.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [250, 260],
                        "coords_fin": [360, 220]
                    }
                },
                {
                    "titulo": "Paso 4: Formación de la enamina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón del Carbono Alfa (C-H)",
                    "smiles_resultado": "CC=CN(C)C",
                    "explicacion": "La base abstrae el protón remanente del carbono alfa, restituyendo la neutralidad del nitrógeno y dando lugar a la enamina.",
                    "imagen_concepto": "Enamina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ],

            # =================================================
            # CICLOHEXANONA
            # =================================================
            "Ciclohexanona": [
                {
                    "titulo": "Paso 1: Ataque nucleofílico",
                    "origen_correcto": "Par libre del Nitrógeno (Amina)",
                    "destino_correcto": "Carbono electrofílico (Carbonilo)",
                    "smiles_resultado": "C1CCC([O-])([N+](C)C)CC1",
                    "explicacion": "Ataque al carbonilo.",
                    "imagen_concepto": "Intermedio dipolar",
                    "flecha": {
                        "coords_inicio": [240, 260],
                        "coords_fin": [350, 210]
                    }
                },
                {
                    "titulo": "Paso 2: Protonación del OH",
                    "origen_correcto": "Par libre del Oxígeno (-OH)",
                    "destino_correcto": "Protón del medio ácido (H3O+)",
                    "smiles_resultado": "C1CCC([OH2+])(N(C)C)CC1",
                    "explicacion": "OH protonado.",
                    "imagen_concepto": "Alcohol protonado",
                    "flecha": {
                        "coords_inicio": [350, 170],
                        "coords_fin": [430, 120]
                    }
                },
                {
                    "titulo": "Paso 3: Formación del ion iminio",
                    "origen_correcto": "Par libre del Nitrógeno",
                    "destino_correcto": "Enlace C-O (Para expulsar H2O)",
                    "smiles_resultado": "C1CCC(=[N+](C)C)CC1",
                    "explicacion": "Salida de agua.",
                    "imagen_concepto": "Ion iminio",
                    "flecha": {
                        "coords_inicio": [240, 250],
                        "coords_fin": [350, 210]
                    }
                },
                {
                    "titulo": "Paso 4: Formación de la enamina",
                    "origen_correcto": "Par libre del Oxígeno (Agua)",
                    "destino_correcto": "Protón del Carbono Alfa (C-H)",
                    "smiles_resultado": "C1CCC(=C)N(C)CC1",
                    "explicacion": "Formación de enamina.",
                    "imagen_concepto": "Enamina final",
                    "flecha": {
                        "coords_inicio": [470, 250],
                        "coords_fin": [360, 250]
                    }
                }
            ]
        }
    }
    # =========================================================
    # INTERFAZ PRINCIPAL
    # =========================================================
    st.title("🧪 Simulador Avanzado de Mecanismos Orgánicos")

    st.markdown("""
    Aprende mecanismos orgánicos trazando correctamente el flujo electrónico.
    """)

    # =========================================================
    # SIDEBAR
    # =========================================================
    st.sidebar.header("⚙️ Configuración")

    opcion_compuesto = st.sidebar.selectbox(
        "1. Selecciona el compuesto:",
        ["Seleccionar...", *SMILES_INICIALES.keys()]
    )

    opcion_reaccion = st.sidebar.selectbox(
        "2. Selecciona el mecanismo:",
        [
            "Seleccionar...",
            "Iminas (Aminas 1°)",
            "Enaminas (Aminas 2°)"
        ]
    )

    # =========================================================
    # REINICIO
    # =========================================================
    if (
        opcion_compuesto != "Seleccionar..."
        and opcion_reaccion != "Seleccionar..."
    ):

        if (
            st.session_state.reaccion != opcion_reaccion
            or st.session_state.sustrato_nombre != opcion_compuesto
        ):

            st.session_state.reaccion = opcion_reaccion
            st.session_state.sustrato_nombre = opcion_compuesto
            st.session_state.paso = 0
            st.session_state.historial = []
            st.session_state.feedback = ""

    # =========================================================
    # EJECUCIÓN PRINCIPAL
    # =========================================================
    if (
        st.session_state.reaccion
        and st.session_state.sustrato_nombre
    ):

        if (
            st.session_state.sustrato_nombre
            not in BASE_MECANISMOS[st.session_state.reaccion]
        ):

            st.warning(
                "⚠️ Ese compuesto aún no tiene mecanismo cargado."
            )

            st.stop()

        pasos = BASE_MECANISMOS[
            st.session_state.reaccion
        ][
            st.session_state.sustrato_nombre
        ]

        idx = st.session_state.paso

        st.header(
            f"📌 {st.session_state.reaccion} con "
            f"{st.session_state.sustrato_nombre}"
        )

        col1, col2 = st.columns([1, 1])

        # =====================================================
        # MOLÉCULA
        # =====================================================
        with col1:

            st.subheader("🔬 Estructura química")

            if idx == 0:

                dibujar_molecula(
                    SMILES_INICIALES[
                        st.session_state.sustrato_nombre
                    ],
                    "Sustrato inicial"
                )

            else:

                paso_actual = pasos[idx - 1]

                dibujar_molecula(
                    paso_actual["smiles_resultado"],
                    paso_actual["imagen_concepto"],
                    paso_actual["flecha"]
                )

        # =====================================================
        # CONTROLES
        # =====================================================
        with col2:

            if idx < len(pasos):

                st.markdown(
                    f"## {pasos[idx]['titulo']}"
                )

                st.info(
                    "🏹 Selecciona correctamente "
                    "el origen y destino del flujo electrónico."
                )

                opciones_origen = [

                    "Seleccionar...",

                    "Par libre del Nitrógeno (Amina)",

                    "Par libre del Nitrógeno",

                    "Par libre del Oxígeno (Alkóxido)",

                    "Par libre del Oxígeno (-OH)",

                    "Par libre del Oxígeno (Agua)",

                    "Enlace doble C=O (Electrones Pi)",

                    "Enlace C-H del Carbono Alfa"
                ]

                opciones_destino = [

                    "Seleccionar...",

                    "Carbono electrofílico (Carbonilo)",

                    "Protón unido al Nitrógeno (H+)",

                    "Protón del medio ácido (H3O+)",

                    "Protón del Carbono Alfa (C-H)",

                    "Enlace C-O (Para expulsar H2O)",

                    "Nitrógeno catiónico"
                ]

                c1, c2 = st.columns(2)

                with c1:

                    origen_usuario = st.selectbox(
                        "🔴 Origen",
                        opciones_origen,
                        key=f"orig_{idx}"
                    )

                with c2:

                    destino_usuario = st.selectbox(
                        "🔵 Destino",
                        opciones_destino,
                        key=f"dest_{idx}"
                    )

                # =================================================
                # BOTÓN
                # =================================================
                if st.button("🚀 Lanzar Flecha"):

                    if (
                        origen_usuario == "Seleccionar..."
                        or destino_usuario == "Seleccionar..."
                    ):

                        st.session_state.feedback = (
                            "⚠️ Debes seleccionar "
                            "origen y destino."
                        )

                    else:

                        valida_origen = (
                            origen_usuario
                            == pasos[idx]["origen_correcto"]
                        )

                        valida_destino = (
                            destino_usuario
                            == pasos[idx]["destino_correcto"]
                        )

                        if valida_origen and valida_destino:

                            st.session_state.feedback = (
                                f"✅ Correcto.\n\n"
                                f"{pasos[idx]['explicacion']}"
                            )

                            st.session_state.historial.append(
                                pasos[idx]["titulo"]
                            )

                            st.session_state.paso += 1

                            st.rerun()

                        else:

                            st.session_state.feedback = (
                                "❌ Movimiento electrónico incorrecto."
                            )

            else:

                st.success(
                    f"🎉 Has completado el mecanismo para "
                    f"{st.session_state.sustrato_nombre}"
                )

                st.balloons()

                if st.button("🔄 Reiniciar"):

                    st.session_state.paso = 0
                    st.session_state.historial = []
                    st.session_state.feedback = ""

                    st.rerun()

        # =====================================================
        # FEEDBACK
        # =====================================================
        st.divider()

        if st.session_state.feedback:

            if "✅" in st.session_state.feedback:

                st.success(st.session_state.feedback)

            elif "⚠️" in st.session_state.feedback:

                st.warning(st.session_state.feedback)

            else:

                st.error(st.session_state.feedback)

        # =====================================================
        # BITÁCORA
        # =====================================================
        st.subheader("📋 Bitácora")

        if st.session_state.historial:

            for h in st.session_state.historial:

                st.write(f"✔️ {h}")

        else:

            st.caption("Aún no hay pasos completados.")


if modulo == "Modulo I":
    ejecutar_modulo1()

elif modulo == "Modulo II":
    ejecutar_modulo2()

elif modulo == "Modulo III":
    ejecutar_modulo3()
