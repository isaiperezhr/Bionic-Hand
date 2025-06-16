import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Paso 1: Cargar el archivo CSV con las características y las etiquetas
features = pd.read_csv('emg_dataset.csv')

# Paso 2: Dividir los datos en características (X) y etiquetas (y)
X = features[['Mean value', 'Std Dev', 'Maximum']]
y = features['Output']

# Paso 3: Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42)

# Modelo de Árbol de Decisión
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)
accuracy_tree = accuracy_score(y_test, y_pred_tree)
print("Precisión del modelo de Árbol de Decisión: {:.2f}".format(
    accuracy_tree))

# Modelo SVM
svm_model = SVC()
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print("Precisión del modelo SVM: {:.2f}".format(accuracy_svm))

# Modelo de Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Precisión del modelo de Random Forest: {:.2f}".format(accuracy_rf))

# Seleccionar el mejor modelo
if accuracy_tree >= accuracy_svm and accuracy_tree >= accuracy_rf:
    best_model = tree_model
    best_preds = y_pred_tree
    model_name = 'decision_tree_model.pkl'
elif accuracy_svm >= accuracy_tree and accuracy_svm >= accuracy_rf:
    best_model = svm_model
    best_preds = y_pred_svm
    model_name = 'svm_model.pkl'
else:
    best_model = rf_model
    best_preds = y_pred_rf
    model_name = 'random_forest_model.pkl'

# Guardar el modelo con mejor precisión
joblib.dump(best_model, model_name)
print("Se ha guardado el modelo con mejor precisión en un archivo pkl:", model_name)

# ==== Sección de gráficas ====
# Matriz de confusión
cm = confusion_matrix(y_test, best_preds)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=sorted(
    y.unique()), yticklabels=sorted(y.unique()))
plt.title(f'Matriz de Confusión - {model_name}')
plt.xlabel('Predicciones')
plt.ylabel('Valores reales')
plt.tight_layout()
plt.show()

# Gráfico de comparación de etiquetas
comparison_df = pd.DataFrame({'Real': y_test.values, 'Predicho': best_preds})
plt.figure(figsize=(10, 5))
# Mostrar solo primeros 30 para visualización clara
comparison_df[:30].plot(kind='bar')
plt.title(f'Comparación etiquetas reales vs predichas - {model_name}')
plt.xlabel('Muestra')
plt.ylabel('Etiqueta')
plt.tight_layout()
plt.show()
