// Multi-language translation dictionary and i18n engine
// Supports: English (en), Spanish (es), French (fr), German (de), Hindi (hi), Kannada (kn), Tamil (ta), Telugu (te)

const TRANSLATIONS = {
  en: {
    // Navigation
    "nav.overview": "Overview",
    "nav.study_planner": "My Study Planner",
    "nav.prediction": "AI Prediction",
    "nav.students": "Students",
    "nav.academic_data": "Academic Data",
    "nav.study_plans_admin": "Study Plans (All)",
    "nav.signin": "Sign in",
    "nav.get_started": "Get started",
    "nav.logout": "Logout",
    "nav.switch_lang": "Language",

    // Headers & Common
    "common.app_title": "AI-Based Academic System",
    "common.welcome": "Welcome back",
    "common.save": "Save",
    "common.cancel": "Cancel",
    "common.close": "Close",
    "common.delete": "Delete",
    "common.edit": "Edit",
    "common.submit": "Submit",
    "common.loading": "Loading...",
    "common.action": "Action",
    "common.status": "Status",
    "common.priority": "Priority",
    "common.date": "Date",
    "common.time": "Time",
    "common.subject": "Subject",
    "common.notes": "Notes",
    "common.all": "All",
    "common.completed": "Completed",
    "common.pending": "Pending",
    "common.high": "High",
    "common.medium": "Medium",
    "common.low": "Low",

    // Student Dashboard
    "dash.title": "Student Dashboard",
    "dash.predicted_marks": "Predicted Marks",
    "dash.attendance": "Attendance",
    "dash.performance": "Performance Status",
    "dash.weekly_study_goal": "Weekly Study Goal",
    "dash.upcoming_exam": "Upcoming Examination",
    "dash.weak_subjects": "Areas for Improvement",
    "dash.strong_subjects": "Strong Subjects",
    "dash.quick_actions": "Quick Actions",
    "dash.open_planner": "Open My Study Planner",
    "dash.run_prediction": "Run New Prediction",
    "dash.no_records": "No academic records linked to this account yet.",

    // Prediction
    "pred.title": "AI Academic Performance Prediction",
    "pred.subtitle": "Estimate expected final examination marks based on your academic assessments and study habits.",
    "pred.internal_marks": "Internal Marks (/100)",
    "pred.assignment_marks": "Assignment Marks (/100)",
    "pred.previous_marks": "Previous Examination Marks (/100)",
    "pred.study_hours": "Average Daily Study Hours",
    "pred.btn_predict": "Predict Final Marks",
    "pred.result_title": "Prediction Result",
    "pred.predicted_final": "Predicted Final Examination Marks",
    "pred.category": "Performance Category",
    "pred.autofill": "Pre-fill from My Subject Records",
    "pred.choose_subject": "-- Choose a subject to prefill --",
    "pred.notice_no_attendance": "Attendance has been removed as an input feature in this predictive model.",

    // Study Planner
    "planner.title": "AI-Powered Personalized Study Planner",
    "planner.subtitle": "Interactive study schedules generated from your academic performance, weak subjects, and upcoming exams.",
    "planner.btn_ai_suggest": "Suggest AI Study Plan",
    "planner.btn_add_task": "Add Study Task",
    "planner.exam_countdown": "Exam Countdown",
    "planner.days_left": "days left",
    "planner.no_upcoming_exam": "No exams scheduled soon",
    "planner.total_scheduled": "Scheduled Hours",
    "planner.completed_hours": "Completed Hours",
    "planner.pending_hours": "Pending Hours",
    "planner.completion_rate": "Completion Rate",
    "planner.view_calendar": "Interactive Calendar",
    "planner.view_timetable": "Daily Timetable",
    "planner.view_weekly": "Weekly Schedule",
    "planner.cal_month": "Month",
    "planner.cal_week": "Week",
    "planner.cal_day": "Day",
    "planner.cal_list": "List / Agenda",
    "planner.cal_today": "Today",
    "planner.cal_prev": "Prev",
    "planner.cal_next": "Next",
    "planner.smart_recommendations": "Intelligent Study Recommendations",
    "planner.reminders_title": "Reminders & Alerts",
    "planner.subject_distribution": "Subject-wise Hours Allocation",
    "planner.priority_subjects": "Priority Subjects",
    "planner.mark_complete": "Mark Complete",
    "planner.mark_pending": "Mark as Pending",
    "planner.reschedule": "Reschedule",
    "planner.delete_task": "Delete Task",
    "planner.no_tasks_today": "No study tasks scheduled for this day.",
    "planner.modal_ai_title": "Generate AI Study Plan",
    "planner.modal_daily_hours": "Available Daily Study Hours",
    "planner.modal_preferred_timing": "Preferred Study Timings",
    "planner.timing_morning": "Morning (06:00 - 09:00)",
    "planner.timing_afternoon": "Afternoon (14:00 - 17:00)",
    "planner.timing_evening": "Evening (18:00 - 21:00)",
    "planner.timing_night": "Night (21:00 - 00:00)",
    "planner.modal_btn_generate": "Generate Personalized Schedule",
    "planner.modal_add_title": "Add Study Task",
    "planner.task_title": "Task Title",
    "planner.topic_name": "Topic / Chapter",
    "planner.duration_mins": "Duration (Minutes)",
    "planner.task_type": "Task Type",
    "planner.type_study": "Concept Study",
    "planner.type_revision": "Revision Session",
    "planner.type_practice": "Practice Test / Past Papers",
    "planner.type_personal": "Personal Task",
    "planner.edit_timing": "Edit Timing & Date",

    // Admin
    "admin.title": "Administrator Dashboard",
    "admin.total_students": "Total Students",
    "admin.avg_performance": "Average Predicted Score",
    "admin.students_support": "Students Needing Support",
    "admin.manage_students": "Manage Students",
    "admin.add_student": "Add Student",
    "admin.search_placeholder": "Search by USN or name",
    "admin.academic_records": "Academic Records"
  },

  es: {
    // Navigation
    "nav.overview": "Resumen",
    "nav.study_planner": "Mi Plan de Estudio",
    "nav.prediction": "Predicción IA",
    "nav.students": "Estudiantes",
    "nav.academic_data": "Datos Académicos",
    "nav.study_plans_admin": "Planes de Estudio (Todos)",
    "nav.signin": "Iniciar Sesión",
    "nav.get_started": "Comenzar",
    "nav.logout": "Cerrar Sesión",
    "nav.switch_lang": "Idioma",

    // Common
    "common.app_title": "Sistema Académico con IA",
    "common.welcome": "Bienvenido",
    "common.save": "Guardar",
    "common.cancel": "Cancelar",
    "common.close": "Cerrar",
    "common.delete": "Eliminar",
    "common.edit": "Editar",
    "common.submit": "Enviar",
    "common.loading": "Cargando...",
    "common.action": "Acción",
    "common.status": "Estado",
    "common.priority": "Prioridad",
    "common.date": "Fecha",
    "common.time": "Hora",
    "common.subject": "Materia",
    "common.notes": "Notas",
    "common.all": "Todos",
    "common.completed": "Completado",
    "common.pending": "Pendiente",
    "common.high": "Alta",
    "common.medium": "Media",
    "common.low": "Baja",

    // Student Dashboard
    "dash.title": "Panel del Estudiante",
    "dash.predicted_marks": "Calificación Estimada",
    "dash.attendance": "Asistencia",
    "dash.performance": "Estado de Rendimiento",
    "dash.weekly_study_goal": "Meta Semanal de Estudio",
    "dash.upcoming_exam": "Próximo Examen",
    "dash.weak_subjects": "Áreas a Mejorar",
    "dash.strong_subjects": "Materias Destacadas",
    "dash.quick_actions": "Acciones Rápidas",
    "dash.open_planner": "Abrir Mi Plan de Estudio",
    "dash.run_prediction": "Ejecutar Nueva Predicción",
    "dash.no_records": "No hay registros académicos vinculados aún.",

    // Prediction
    "pred.title": "Predicción de Rendimiento Académico con IA",
    "pred.subtitle": "Estima tu nota final esperada basada en evaluaciones académicas y hábitos de estudio.",
    "pred.internal_marks": "Notas Internas (/100)",
    "pred.assignment_marks": "Notas de Tareas (/100)",
    "pred.previous_marks": "Notas de Exámenes Previos (/100)",
    "pred.study_hours": "Horas Diarias Promedio de Estudio",
    "pred.btn_predict": "Predecir Calificación Final",
    "pred.result_title": "Resultado de la Predicción",
    "pred.predicted_final": "Calificación Final Estimada",
    "pred.category": "Categoría de Rendimiento",
    "pred.autofill": "Rellenar desde Mis Materias",
    "pred.choose_subject": "-- Elegir materia para rellenar --",
    "pred.notice_no_attendance": "La asistencia ha sido eliminada como característica de entrada en este modelo.",

    // Study Planner
    "planner.title": "Planificador de Estudio Personalizado con IA",
    "planner.subtitle": "Horarios de estudio interactivos generados a partir de tu rendimiento académico, materias débiles y próximos exámenes.",
    "planner.btn_ai_suggest": "Sugerir Plan con IA",
    "planner.btn_add_task": "Añadir Tarea",
    "planner.exam_countdown": "Cuenta Regresiva para Exámenes",
    "planner.days_left": "días restantes",
    "planner.no_upcoming_exam": "Sin exámenes cercanos",
    "planner.total_scheduled": "Horas Programadas",
    "planner.completed_hours": "Horas Completadas",
    "planner.pending_hours": "Horas Pendientes",
    "planner.completion_rate": "Tasa de Finalización",
    "planner.view_calendar": "Calendario Interactivo",
    "planner.view_timetable": "Horario Diario",
    "planner.view_weekly": "Horario Semanal",
    "planner.cal_month": "Mes",
    "planner.cal_week": "Semana",
    "planner.cal_day": "Día",
    "planner.cal_list": "Agenda",
    "planner.cal_today": "Hoy",
    "planner.cal_prev": "Ant",
    "planner.cal_next": "Sig",
    "planner.smart_recommendations": "Recomendaciones Inteligentes de Estudio",
    "planner.reminders_title": "Recordatorios y Alertas",
    "planner.subject_distribution": "Distribución de Horas por Materia",
    "planner.priority_subjects": "Materias Prioritarias",
    "planner.mark_complete": "Marcar Completado",
    "planner.mark_pending": "Marcar como Pendiente",
    "planner.reschedule": "Reprogramar",
    "planner.delete_task": "Eliminar Tarea",
    "planner.no_tasks_today": "No hay tareas programadas para este día.",
    "planner.modal_ai_title": "Generar Plan de Estudio con IA",
    "planner.modal_daily_hours": "Horas Diarias de Estudio Disponibles",
    "planner.modal_preferred_timing": "Horario Preferido",
    "planner.timing_morning": "Mañana (06:00 - 09:00)",
    "planner.timing_afternoon": "Tarde (14:00 - 17:00)",
    "planner.timing_evening": "Noche (18:00 - 21:00)",
    "planner.timing_night": "Madrugada (21:00 - 00:00)",
    "planner.modal_btn_generate": "Generar Horario Personalizado",
    "planner.modal_add_title": "Añadir Tarea de Estudio",
    "planner.task_title": "Título de la Tarea",
    "planner.topic_name": "Tema / Capítulo",
    "planner.duration_mins": "Duración (Minutos)",
    "planner.task_type": "Tipo de Tarea",
    "planner.type_study": "Estudio de Conceptos",
    "planner.type_revision": "Sesión de Repaso",
    "planner.type_practice": "Prueba de Práctica",
    "planner.type_personal": "Tarea Personal",
    "planner.edit_timing": "Editar Hora y Fecha",

    // Admin
    "admin.title": "Panel de Administración",
    "admin.total_students": "Total de Estudiantes",
    "admin.avg_performance": "Puntuación Promedio Estimada",
    "admin.students_support": "Estudiantes con Necesidad de Apoyo",
    "admin.manage_students": "Gestionar Estudiantes",
    "admin.add_student": "Añadir Estudiante",
    "admin.search_placeholder": "Buscar por USN o nombre",
    "admin.academic_records": "Registros Académicos"
  },

  fr: {
    "nav.overview": "Vue d'ensemble",
    "nav.study_planner": "Mon Planificateur",
    "nav.prediction": "Prédiction IA",
    "nav.students": "Étudiants",
    "nav.academic_data": "Données Académiques",
    "nav.study_plans_admin": "Plans d'Étude (Tous)",
    "nav.signin": "Se connecter",
    "nav.get_started": "Commencer",
    "nav.logout": "Déconnexion",
    "nav.switch_lang": "Langue",
    "common.app_title": "Système Académique IA",
    "dash.title": "Tableau de Bord Étudiant",
    "pred.title": "Prédiction des Performances Académiques par IA",
    "planner.title": "Planificateur d'Études Personnalisé par IA",
    "planner.btn_ai_suggest": "Suggérer un Plan par IA",
    "planner.btn_add_task": "Ajouter une Tâche",
    "planner.cal_today": "Aujourd'hui",
    "common.completed": "Terminé",
    "common.pending": "En attente"
  },

  de: {
    "nav.overview": "Übersicht",
    "nav.study_planner": "Mein Lernplaner",
    "nav.prediction": "KI-Vorhersage",
    "nav.students": "Studenten",
    "nav.academic_data": "Akademische Daten",
    "nav.study_plans_admin": "Lernpläne (Alle)",
    "nav.signin": "Anmelden",
    "nav.get_started": "Loslegen",
    "nav.logout": "Abmelden",
    "nav.switch_lang": "Sprache",
    "common.app_title": "KI-Akademisches System",
    "dash.title": "Studenten-Dashboard",
    "pred.title": "KI-Leistungsvorhersage",
    "planner.title": "KI-Personalisierter Studienplaner",
    "planner.btn_ai_suggest": "KI-Lernplan vorschlagen",
    "planner.btn_add_task": "Lernaufgabe hinzufügen",
    "planner.cal_today": "Heute",
    "common.completed": "Abgeschlossen",
    "common.pending": "Ausstehend"
  },

  hi: {
    // Navigation
    "nav.overview": "अवलोकन (Overview)",
    "nav.study_planner": "मेरा स्टडी प्लानर",
    "nav.prediction": "एआई प्रदर्शन भविष्यवाणी",
    "nav.students": "छात्र सूची",
    "nav.academic_data": "अकादमिक डेटा",
    "nav.study_plans_admin": "सभी स्टडी प्लान्स",
    "nav.signin": "साइन इन करें",
    "nav.get_started": "शुरू करें",
    "nav.logout": "लॉग आउट",
    "nav.switch_lang": "भाषा (Language)",

    // Common
    "common.app_title": "एआई आधारित अकादमिक प्रणाली",
    "common.welcome": "स्वागत है",
    "common.save": "सहेजें (Save)",
    "common.cancel": "रद्द करें",
    "common.close": "बंद करें",
    "common.delete": "हटाएं",
    "common.edit": "संपादित करें",
    "common.submit": "जमा करें",
    "common.loading": "लोड हो रहा है...",
    "common.action": "कार्रवाई",
    "common.status": "स्थिति",
    "common.priority": "प्राथमिकता",
    "common.date": "तारीख",
    "common.time": "समय",
    "common.subject": "विषय",
    "common.notes": "टिप्पणी",
    "common.all": "सभी",
    "common.completed": "पूर्ण (Completed)",
    "common.pending": "लंबित (Pending)",
    "common.high": "उच्च (High)",
    "common.medium": "मध्यम (Medium)",
    "common.low": "निम्न (Low)",

    // Student Dashboard
    "dash.title": "छात्र डैशबोर्ड",
    "dash.predicted_marks": "अनुमानित अंक",
    "dash.attendance": "उपस्थिति",
    "dash.performance": "प्रदर्शन स्थिति",
    "dash.weekly_study_goal": "साप्ताहिक अध्ययन लक्ष्य",
    "dash.upcoming_exam": "आगामी परीक्षा",
    "dash.weak_subjects": "सुधार के क्षेत्र (कमजोर विषय)",
    "dash.strong_subjects": "मजबूत विषय",
    "dash.quick_actions": "त्वरित क्रियाएं",
    "dash.open_planner": "स्टडी प्लानर खोलें",
    "dash.run_prediction": "नई भविष्यवाणी चलाएं",
    "dash.no_records": "इस खाते से अभी कोई अकादमिक रिकॉर्ड जुड़ा नहीं है।",

    // Prediction
    "pred.title": "एआई अकादमिक प्रदर्शन भविष्यवाणी",
    "pred.subtitle": "अपने आंतरिक मूल्यांकन और अध्ययन आदतों के आधार पर अंतिम परीक्षा अंक का अनुमान लगाएं।",
    "pred.internal_marks": "आंतरिक अंक (/100)",
    "pred.assignment_marks": "असाइनमेंट अंक (/100)",
    "pred.previous_marks": "पिछली परीक्षा के अंक (/100)",
    "pred.study_hours": "औसत दैनिक अध्ययन घंटे",
    "pred.btn_predict": "अंतिम अंकों की भविष्यवाणी करें",
    "pred.result_title": "भविष्यवाणी परिणाम",
    "pred.predicted_final": "अनुमानित अंतिम परीक्षा अंक",
    "pred.category": "प्रदर्शन श्रेणी",
    "pred.autofill": "मेरे विषय रिकॉर्ड से भरें",
    "pred.choose_subject": "-- विषय चुनें --",
    "pred.notice_no_attendance": "इस मॉडल में उपस्थिति (Attendance) को इनपुट से हटा दिया गया है।",

    // Study Planner
    "planner.title": "एआई-संचालित व्यक्तिगत स्टडी प्लानर",
    "planner.subtitle": "आपके वास्तविक अकादमिक प्रदर्शन, कमजोर विषयों और आगामी परीक्षाओं के आधार पर स्वचालित अध्ययन अनुसूची।",
    "planner.btn_ai_suggest": "एआई से स्टडी प्लान का सुझाव लें",
    "planner.btn_add_task": "नया अध्ययन कार्य जोड़ें",
    "planner.exam_countdown": "परीक्षा उल्टी गिनती",
    "planner.days_left": "दिन शेष",
    "planner.no_upcoming_exam": "जल्द कोई परीक्षा नहीं है",
    "planner.total_scheduled": "कुल निर्धारित घंटे",
    "planner.completed_hours": "पूर्ण किए गए घंटे",
    "planner.pending_hours": "लंबित घंटे",
    "planner.completion_rate": "पूर्णता दर",
    "planner.view_calendar": "इंटरैक्टिव कैलेंडर",
    "planner.view_timetable": "दैनिक समय सारिणी",
    "planner.view_weekly": "साप्ताहिक अनुसूची",
    "planner.cal_month": "महीना",
    "planner.cal_week": "सप्ताह",
    "planner.cal_day": "दिन",
    "planner.cal_list": "सूची / कार्य",
    "planner.cal_today": "आज (Today)",
    "planner.cal_prev": "पिछला",
    "planner.cal_next": "अगला",
    "planner.smart_recommendations": "बुद्धिमान अध्ययन सिफारिशें (AI Recommendations)",
    "planner.reminders_title": "स्मरणपत्र एवं सूचनाएं (Alerts)",
    "planner.subject_distribution": "विषय-वार अध्ययन समय वितरण",
    "planner.priority_subjects": "प्राथमिकता वाले विषय",
    "planner.mark_complete": "पूर्ण चिह्नित करें",
    "planner.mark_pending": "लंबित चिह्नित करें",
    "planner.reschedule": "पुनर्निर्धारित करें",
    "planner.delete_task": "कार्य हटाएं",
    "planner.no_tasks_today": "इस दिन के लिए कोई कार्य निर्धारित नहीं है।",
    "planner.modal_ai_title": "एआई स्टडी प्लान उत्पन्न करें",
    "planner.modal_daily_hours": "दैनिक उपलब्ध अध्ययन घंटे",
    "planner.modal_preferred_timing": "पसंदीदा अध्ययन समय",
    "planner.timing_morning": "सुबह (06:00 - 09:00)",
    "planner.timing_afternoon": "दोपहर (14:00 - 17:00)",
    "planner.timing_evening": "शाम (18:00 - 21:00)",
    "planner.timing_night": "रात (21:00 - 00:00)",
    "planner.modal_btn_generate": "व्यक्तिगत अनुसूची उत्पन्न करें",
    "planner.modal_add_title": "अध्ययन कार्य जोड़ें",
    "planner.task_title": "कार्य शीर्षक",
    "planner.topic_name": "विषय / अध्याय",
    "planner.duration_mins": "अवधि (मिनट)",
    "planner.task_type": "कार्य का प्रकार",
    "planner.type_study": "अवधारणा अध्ययन",
    "planner.type_revision": "पुनरीक्षण (रिवीजन)",
    "planner.type_practice": "अभ्यास परीक्षा",
    "planner.type_personal": "व्यक्तिगत कार्य",
    "planner.edit_timing": "समय और तारीख संपादित करें",

    // Admin
    "admin.title": "प्रशासक डैशबोर्ड",
    "admin.total_students": "कुल छात्र",
    "admin.avg_performance": "औसत अनुमानित स्कोर",
    "admin.students_support": "सहायता की आवश्यकता वाले छात्र",
    "admin.manage_students": "छात्र प्रबंधन",
    "admin.add_student": "छात्र जोड़ें",
    "admin.search_placeholder": "यूएसएन या नाम से खोजें",
    "admin.academic_records": "अकादमिक रिकॉर्ड्स"
  },

  kn: {
    // Kannada
    "nav.overview": "ಅವಲೋಕನ",
    "nav.study_planner": "ನನ್ನ ಅಧ್ಯಯನ ಯೋಜಕ (Study Planner)",
    "nav.prediction": "ಎಐ ಭವಿಷ್ಯವಾಣಿ (Prediction)",
    "nav.students": "ವಿದ್ಯಾರ್ಥಿಗಳು",
    "nav.academic_data": "ಶೈಕ್ಷಣಿಕ ವಿವರ",
    "nav.study_plans_admin": "ಅಧ್ಯಯನ ಯೋಜನೆಗಳು (ಎಲ್ಲಾ)",
    "nav.signin": "ಸೈನ್ ಇನ್",
    "nav.get_started": "ಪ್ರಾರಂಭಿಸಿ",
    "nav.logout": "ಲಾಗ್ ಔಟ್",
    "nav.switch_lang": "ಭಾಷೆ (Language)",

    "common.app_title": "ಎಐ ಆಧಾರಿತ ಶೈಕ್ಷಣಿಕ ವ್ಯವಸ್ಥೆ",
    "common.welcome": "ಸುಸ್ವಾಗತ",
    "common.save": "ಉಳಿಸಿ",
    "common.cancel": "ರದ್ದುಮಾಡಿ",
    "common.close": "ಮುಚ್ಚಿ",
    "common.delete": "ಅಳಿಸಿ",
    "common.edit": "ತಿದ್ದಿ",
    "common.submit": "ಸಲ್ಲಿಸಿ",
    "common.completed": "ಪೂರ್ಣಗೊಂಡಿದೆ",
    "common.pending": "ಬಾಕಿ ಉಳಿದಿದೆ",
    "common.high": "ಹೆಚ್ಚು",
    "common.medium": "ಮಧ್ಯಮ",
    "common.low": "ಕಡಿಮೆ",

    "dash.title": "ವಿದ್ಯಾರ್ಥಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    "dash.predicted_marks": "ಅಂದಾಜು ಅಂಕಗಳು",
    "dash.attendance": "ಹಾಜರಾತಿ",
    "dash.performance": "ಸಾಮರ್ಥ್ಯ ಸ್ಥಿತಿ",
    "dash.upcoming_exam": "ಮುಂಬರುವ ಪರೀಕ್ಷೆ",
    "dash.open_planner": "ಅಧ್ಯಯನ ಯೋಜಕ ತೆರೆಯಿರಿ",

    "pred.title": "ಎಐ ಶೈಕ್ಷಣಿಕ ಸಾಧನೆ ಮುನ್ಸೂಚನೆ",
    "pred.internal_marks": "ಇಂಟರ್ನಲ್ ಅಂಕಗಳು (/100)",
    "pred.assignment_marks": "ಅಸೈನ್‌ಮೆಂಟ್ ಅಂಕಗಳು (/100)",
    "pred.previous_marks": "ಹಿಂದಿನ ಪರೀಕ್ಷಾ ಅಂಕಗಳು (/100)",
    "pred.study_hours": "ದೈನಂದಿನ ಅಧ್ಯಯನ ಗಂಟೆಗಳು",
    "pred.btn_predict": "ಅಂತಿಮ ಅಂಕಗಳನ್ನು ಅಂದಾಜಿಸಿ",
    "pred.notice_no_attendance": "ಈ ಮುನ್ಸೂಚನೆ ಮಾದರಿಯಿಂದ ಹಾಜರಾತಿಯನ್ನು ತೆಗೆದುಹಾಕಲಾಗಿದೆ.",

    "planner.title": "ಎಐ ಆಧಾರಿತ ವೈಯಕ್ತಿಕ ಅಧ್ಯಯನ ಯೋಜಕ",
    "planner.subtitle": "ನಿಮ್ಮ ಶೈಕ್ಷಣಿಕ ಪ್ರಗತಿ ಮತ್ತು ಮುಂಬರುವ ಪರೀಕ್ಷೆಗಳ ಆಧಾರದ ಮೇಲೆ ವೈಯಕ್ತಿಕ ವೇಳಾಪಟ್ಟಿ.",
    "planner.btn_ai_suggest": "ಎಐ ಯೋಜನೆ ಸಲಹೆ ಪಡೆಯಿರಿ",
    "planner.btn_add_task": "ಹೊಸ ಅಧ್ಯಯನ ಕೆಲಸ ಸೇರಿಸಿ",
    "planner.exam_countdown": "ಪರೀಕ್ಷಾ ಕೌಂಟ್‌ಡೌನ್",
    "planner.days_left": "ದಿನಗಳು ಬಾಕಿ",
    "planner.total_scheduled": "ನಿಗದಿತ ಗಂಟೆಗಳು",
    "planner.completed_hours": "ಪೂರ್ಣಗೊಂಡ ಗಂಟೆಗಳು",
    "planner.view_calendar": "ಕ್ಯಾಲೆಂಡರ್ ವೀಕ್ಷಣೆ",
    "planner.cal_today": "ಇಂದು",
    "planner.cal_month": "ತಿಂಗಳು",
    "planner.cal_week": "ವಾರ",
    "planner.cal_day": "ದಿನ",
    "planner.smart_recommendations": "ಬುದ್ಧಿವಂತ ಅಧ್ಯಯನ ಶಿಫಾರಸುಗಳು",
    "planner.modal_ai_title": "ಎಐ ಅಧ್ಯಯನ ವೇಳಾಪಟ್ಟಿ ರಚಿಸಿ"
  },

  ta: {
    // Tamil
    "nav.overview": "கண்ணோட்டம்",
    "nav.study_planner": "என் படிப்பு திட்டமிடுபவர்",
    "nav.prediction": "AI கணிப்பு",
    "nav.students": "மாணவர்கள்",
    "nav.academic_data": "கல்வித் தரவு",
    "nav.signin": "உள்நுழைய",
    "nav.get_started": "தொடங்குங்கள்",
    "nav.logout": "வெளியேறு",
    "nav.switch_lang": "மொழி",
    "dash.title": "மாணவர் கட்டுப்பாட்டு பலகை",
    "pred.title": "AI கல்வி செயல்திறன் கணிப்பு",
    "planner.title": "AI இயங்கும் தனிப்பயனாக்கப்பட்ட படிப்பு திட்டம்",
    "planner.btn_ai_suggest": "AI ஆய்வுத் திட்டத்தை உருவாக்குங்கள்",
    "planner.btn_add_task": "புதிய பணியைச் சேர்க்கவும்",
    "common.completed": "முடிந்தது",
    "common.pending": "நிலுவையில் உள்ளது"
  },

  te: {
    // Telugu
    "nav.overview": "అవలోకనం",
    "nav.study_planner": "నా స్టడీ ప్లానర్",
    "nav.prediction": "AI ప్రిడిక్షన్",
    "nav.students": "విద్యార్థులు",
    "nav.academic_data": "విద్యా సమాచారం",
    "nav.signin": "సైన్ ఇన్",
    "nav.get_started": "ప్రారంభించండి",
    "nav.logout": "లాగ్ అవుట్",
    "nav.switch_lang": "భాష",
    "dash.title": "విద్యార్థి డాష్‌బోర్డ్",
    "pred.title": "AI అకడమిక్ పనితీరు అంచనా",
    "planner.title": "AI వ్యక్తిగతీకరించిన స్టడీ ప్లానర్",
    "planner.btn_ai_suggest": "AI స్టడీ ప్లాన్‌ని సూచించండి",
    "planner.btn_add_task": "స్టడీ టాస్క్ జోడించండి",
    "common.completed": "పూర్తయింది",
    "common.pending": "పెండింగ్‌లో ఉంది"
  }
};

class I18nManager {
  constructor() {
    this.currentLang = localStorage.getItem("app_language") || "en";
    this.init();
  }

  init() {
    this.applyLanguage(this.currentLang);
    this.setupDropdownListeners();
  }

  setLanguage(lang) {
    if (!TRANSLATIONS[lang]) lang = "en";
    this.currentLang = lang;
    localStorage.setItem("app_language", lang);

    // Also inform the backend session asynchronously
    fetch("/api/set-language", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language: lang })
    }).catch(() => {});

    this.applyLanguage(lang);
  }

  t(key, fallback = null) {
    const dict = TRANSLATIONS[this.currentLang] || TRANSLATIONS.en;
    if (dict[key]) return dict[key];
    if (TRANSLATIONS.en[key]) return TRANSLATIONS.en[key];
    return fallback !== null ? fallback : key;
  }

  applyLanguage(lang) {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
    const fallbackDict = TRANSLATIONS.en;

    // Update text for all elements with data-i18n attribute
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      const translation = dict[key] || fallbackDict[key];
      if (translation) {
        if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
          el.placeholder = translation;
        } else {
          el.textContent = translation;
        }
      }
    });

    // Update placeholders for elements with data-i18n-placeholder
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      const translation = dict[key] || fallbackDict[key];
      if (translation) el.placeholder = translation;
    });

    // Update title attributes for elements with data-i18n-title
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      const key = el.getAttribute("data-i18n-title");
      const translation = dict[key] || fallbackDict[key];
      if (translation) el.title = translation;
    });

    // Update active state in language selector UI
    document.querySelectorAll(".lang-option").forEach(opt => {
      if (opt.getAttribute("data-lang") === lang) {
        opt.classList.add("active");
      } else {
        opt.classList.remove("active");
      }
    });

    const currentLangLabel = document.getElementById("current-lang-label");
    if (currentLangLabel) {
      const labels = {
        en: "English",
        es: "Español",
        fr: "Français",
        de: "Deutsch",
        hi: "हिन्दी",
        kn: "ಕನ್ನಡ",
        ta: "தமிழ்",
        te: "తెలుగు"
      };
      currentLangLabel.textContent = labels[lang] || "English";
    }

    // Trigger custom event for dynamic components (like the calendar)
    window.dispatchEvent(new CustomEvent("languageChanged", { detail: { lang } }));
  }

  setupDropdownListeners() {
    document.addEventListener("click", e => {
      const target = e.target.closest(".lang-option");
      if (target) {
        e.preventDefault();
        const selectedLang = target.getAttribute("data-lang");
        if (selectedLang) {
          this.setLanguage(selectedLang);
        }
      }
    });
  }
}

// Global instance
window.i18n = new I18nManager();
