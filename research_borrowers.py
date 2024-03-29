#!/usr/bin/env python
# coding: utf-8

# Привет! Меня зовут Арина, я буду ревьюером твоего проекта. Ты можешь обращаться ко мне на "ты". Пожалуйста, не удаляй мои комментарии, они будут особенно полезны для нашей работы в случае повторной проверки проекта. Ты также можешь реагировать на мои комментарии своими заметками и изменениями, выделяя их цветами и наиболее понравившимся тебе способом оформления!😉
# 
# 
# Ты можешь найти мои комментарии, обозначенные <font color='green'>зеленым</font>, <font color='yellow'>желтым</font> и <font color='red'>красным</font> цветами, например:

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> В случае, если решение задач на отдельном шаге является полностью правильным.
# </div>

# <div class="alert alert-warning">
#     <h2> Комментарий ревьюера</h2>
# 
# <b>Некоторые замечания💡:</b> В случае, когда решение задач на отдельном шаге станет еще лучше, если внести небольшие и некритичные коррективы.
# </div>

# <div class="alert alert-block alert-danger">
# <h2> Комментарий ревьюера</h2>
#     
# <b>На доработку🤔:</b> В случае, когда задачи на отдельном шаге требуют существенной доработки и внесения правок. Напоминаю, что проект не может быть принят с первого раза, если ревью содержит комментарии, рекомендующие доработку проекта.
# </div>

# ## Исследование надёжности заёмщиков
# 
# Заказчик — кредитный отдел банка. Нужно разобраться, влияет ли семейное положение и количество детей клиента на факт погашения кредита в срок. Входные данные от банка — статистика о платёжеспособности клиентов.
# 
# Результаты исследования будут учтены при построении модели **кредитного скоринга** — специальной системы, которая оценивает способность потенциального заёмщика вернуть кредит банку.

# <a href='#Общая информация по таблице'>Общая информация по таблице</a>

# <a href='#Обработка пропусков'>Обработка пропусков</a>

# <a href='#Замена типа данных'>Замена типа данных</a>

# <a href='#Обработка дубликатов'>Обработка дубликатов</a>

# <a href='#Лемматизация'>Лемматизация</a>

# <a href='#Категоризация данных'>Категоризация данных</a>

# <a href='#Ответы на вопросы'>Ответы на вопросы</a>

# <a href='#Общий вывод'>Общий вывод</a>

# ### Шаг 1. Откройте файл с данными и изучите общую информацию. 

# In[4]:


import pandas as pd
df=pd.read_csv('/datasets/data.csv')
df.head(15)


# #### 1.1 Описание данных:
# * children - количество детей в семье;
# * days_employed - общий трудовой стаж в семье;
# * dob_years - возраст клиента;
# * education - уровень образования клиента;
# * education_id - идентификатор уровня образования;
# * family_status - семейное положение;
# * family_status_id - идентификатор семейного положения;
# * gender - пол клиента;
# * income_type - тип занятости;
# * debt - имел ли задолженность по возврату кредитов;
# * total_income - ежемесячный доход;
# * purpose - цель получения кредита

# #### 1.2 Изучим общую информацию по данным кредитного отдела банка:
# 
# * с помощью функции info() получим общую информацию о таблице;
# * с помощью функции describe() получим общие статистические данные для каждого столбца таблицы.
# 

# In[5]:


df.info()


# ##### Комментарий 1. 
# * таблица с данными состоит из 21525 строк и 12 столбцов;
# * в столбцах days_employed и total_income есть отсутствующие значения. Возможно, клиенты банка отказались предоставлять информацию или данные затерялись/некорректно отобразились. Так как нет возможности обратиться к инженеру проекта, буду считать, что клиенты отказались предоставлять информацию и заполню пропущенные ячейки самостоятельно, исходя из доступных данных таблицы;
# * тип данных в столбцах days_employed и total_income - вещественный, подобная точность нам не нужна, заменим на целочисленный с помощью функции astype(), в остальных столбцах тип данных корректный;
# * наименования столбцов соответсвуют их содержанию, воспользуемся функцией set_axis(), чтобы комфортно работать с данными без возможных ошибок. 
# 

# In[6]:


#исключим пропуски в наименовании столбцов, для этого переименуем их и сохраним данные в исх. таблице
df.set_axis(['children', 'days_employed', 'dob_years', 'education', 'education_id', 'family_status', 'family_status_id', 'gender', 'income_type', 'debt', 'total_income', 'purpose'], axis='columns', inplace=True)
df.columns


# In[7]:


df.describe() 


# ##### Комментарий 2.
# * В столбце children min значение -1, в данные закралась ошибка, исправим ее, взяв значения этого столбца по модулю с помощью функции abs();
# * В столбце days_employed есть отрицательные значения, в данные закралась ошибка, исправим ее, взяв значения этого столбца по модулю;
# * В столбце children max значение 20 - это очень много, проверим, у какого количества клиентов такие данные с помощью функции count(), чтобы избежать ошибок;
# * min значение в столбце dob_years = 0, скорее всего это ошибка, в реальной жизни можно обратиться к инженеру проекта за разъяснением, посмотрим, в каком количестве данных содержится ошибка с помощью функции count().
# 

# In[8]:


#заменим отрицательные значения в столбце days_employed и children на положительные
df['days_employed'] = df['days_employed'].abs()
df['children'] = df['children'].abs()
print(df.loc[df['children'] == 20]['children'].count())
print(df.loc[df['dob_years'] == 0]['dob_years'].count())


# #### Вывод:
# * исправили отрицательные значения в столбцах на положительные;
# * подготовили названия столбцов для дальнейшей работы;
# * обнаруженные ошибки в столбцах dob_years и children содержатся менее, чем в 1% от общего объема данных, соответственно, на итоговые результаты исследования не должны повлиять, поэтому оставим без изменений.
# 
# #### Для дальнейшей работы:
# * необходимо обработать пропуски в данных;
# * изменить тип данных в столбцах days_employed и total_income на целочисленный;
# * привести значения столбца education к нижнему регистру, чтобы можно было в дальнейшем работать с данными.

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Хорошая работа! Здорово, что ты уделила внимание всем аномалиям в данных, попыталась не только исправить их технически, но и дать интерпретацию причин таких аномалий. Так держать!
# </div>

# ### Шаг 2. Предобработка данных

# ### Обработка пропусков
# 
# 
# 
# 

# * посчитаем долю пропусков в столбцах с помощью функции mean();
# * проверим, пропуски в столбцах в одних и тех же строках или в разных с помощью условия.

# In[9]:


#считаем долю пропусков в столбцах
df.isnull().mean()


# ##### Комментарий 1.
# 
# В столбцах days_employed и total_income доля пропусков чуть больше 1%, это немного, но если их удалить, то потеряется информация из других столбцов, следовательно, целесообразнее будет их заполнить и после уже анализировать таблицу 

# In[10]:


#проверяем, совпадают ли строки с пропусками
df[(df['days_employed'].isnull() == True) & (df['total_income'].isnull() == True)].count()


# ##### Комментарий 2.
# 
# Да, строки с пропущенными данными совпадают в столбцах days_employed и total_income. Интересное наблюдение, можно предположить, что клиенты просто отказались эти данные предоставлять.

# In[11]:


#Заполним пропущенные значения в столбцах характерными значениями, используя метод median(), для этого сгруппируем таблицу по столбцу income_type
m_table = df.groupby(['income_type']).agg({'total_income' : 'median'})
m_table


# In[12]:


df.loc[df['income_type'] == 'безработный', 'total_income'] = df.loc[df['income_type'] == 'безработный', 'total_income'].fillna(131339.751676)
df.loc[df['income_type'] == 'в декрете', 'total_income'] = df.loc[df['income_type'] == 'в декрете', 'total_income'].fillna(53829.130729)
df.loc[df['income_type'] == 'госслужащий', 'total_income'] = df.loc[df['income_type'] == 'госслужащий', 'total_income'].fillna(150447.935283)
df.loc[df['income_type'] == 'компаньон', 'total_income'] = df.loc[df['income_type'] == 'компаньон', 'total_income'].fillna(172357.950966)
df.loc[df['income_type'] == 'пенсионер', 'total_income'] = df.loc[df['income_type'] == 'пенсионер', 'total_income'].fillna(118514.486412)
df.loc[df['income_type'] == 'предприниматель', 'total_income'] = df.loc[df['income_type'] == 'предприниматель', 'total_income'].fillna(499163.144947)
df.loc[df['income_type'] == 'сотрудник', 'total_income'] = df.loc[df['income_type'] == 'сотрудник', 'total_income'].fillna(142594.396847)
df.loc[df['income_type'] == 'студент', 'total_income'] = df.loc[df['income_type'] == 'студент', 'total_income'].fillna(98201.625314)


# ##### Итог 1.
# Заменили пропущенные значения столбца total_income на медианные значения в зависимости от income_type

# In[13]:


#Заменим таким же образом пропущенные значения в столбце days_employed
m_table = df.groupby(['income_type']).agg({'days_employed' : 'median'})
m_table


# In[14]:


df.loc[df['income_type'] == 'безработный', 'days_employed'] = df.loc[df['income_type'] == 'безработный', 'days_employed'].fillna(366413.652744)
df.loc[df['income_type'] == 'в декрете', 'days_employed'] = df.loc[df['income_type'] == 'в декрете', 'days_employed'].fillna(3296.759962)
df.loc[df['income_type'] == 'госслужащий', 'days_employed'] = df.loc[df['income_type'] == 'госслужащий', 'days_employed'].fillna(2689.368353)
df.loc[df['income_type'] == 'компаньон', 'days_employed'] = df.loc[df['income_type'] == 'компаньон', 'days_employed'].fillna(1547.382223)
df.loc[df['income_type'] == 'пенсионер', 'days_employed'] = df.loc[df['income_type'] == 'пенсионер', 'days_employed'].fillna(365213.306266)
df.loc[df['income_type'] == 'предприниматель', 'days_employed'] = df.loc[df['income_type'] == 'предприниматель', 'days_employed'].fillna(520.848083)
df.loc[df['income_type'] == 'сотрудник', 'days_employed'] = df.loc[df['income_type'] == 'сотрудник', 'days_employed'].fillna(1574.202821)
df.loc[df['income_type'] == 'студент', 'days_employed'] = df.loc[df['income_type'] == 'студент', 'days_employed'].fillna(578.751554)


# ##### Итог 2.
# Заменили пропущенные значения столбца days_employed на медианные значения в зависимости от income_type

# In[15]:


#проверка исходной таблицы на пропущенные значения
df.info()


# #### Вывод:
# Заменили пропущенные значения столбца total_income и  days_employed на медианные значения в зависимости от income_type, теперь все данные в таблице заполнены без пропусков и корректно.
# 
# #### Для дальнейшей работы:
# * изменить тип данных в столбцах days_employed и total_income на целочисленный;
# * привести значения столбца education к нижнему регистру, чтобы можно было в дальнейшем работать с данными;
# * проверить таблицу на наличие дубликатов;
# * для определения зависимости целей кредита и его просрочки, нам нужно будет выделить несколько основных целей, провести лемматизацию с исходными данными таблицы и создать новый столбец с более краткими целями, по которым можно будет провести анализ.
# 

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Ты выбрала интересный способ замены пропущенных значений! Для более лаконичного и удобного для дальнейшего применения кода, можно попробовать автоматизировать замену пропущенных значений в интересующих нас столбцах на медианные значения в зависимости от другого показателя с помощью цикла  ветвления. Автоматизировать свои решения - это хорошая практика!😉
# </div>

# <a id='Замена типа данных'></a>
# ### Замена типа данных

# * изменим тип данных в столбцах days_employed и total_income на целочисленный
# * приведем значения столбца education к нижнему регистру, чтобы можно было в дальнейшем категоризировать клиентов по данному столбцу

# In[16]:


#изменим тип столбцов total_income иdays_employed на int
df['total_income'] = df['total_income'].astype('int')
df['days_employed'] = df['days_employed'].astype('int')

#проверка
df.dtypes


# In[17]:


#приведем все значения столбца education в нижний регистр
df['education']=df['education'].str.lower()

#проверка
df['education'].unique()


# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Шаг выполнен корректно, ты молодец! Очень хорошо, что значения типа object были приведены тобой к нижнему регистру. Это отличная практика, которая в некоторых случаях помогает избежать проблем при работе с данными.
# </div>

# <a id='Обработка дубликатов'></a>
# ### Обработка дубликатов

# In[18]:


df.duplicated().sum()


# ##### Комментарий 3.
# 
# Так как в исходных данных нет id пользователя, будем считать, что данные и правда продублировались, для их удаления будем использовать метод drop_duplicates(), присвоим новые индексы для данных с помощью метода reset_index(drop=True)

# In[19]:


df=df.drop_duplicates().reset_index(drop=True)


# In[20]:


#проверка
df.duplicated().sum()


# #### Вывод:
# 
# В исходной таблице мы нашли 71 строку с дубликатами, скорее всего, это все данные одного человека, но так как в данных нет id клиента, узнать наверняка мы не можем, после обработки дубликатов в таблице остались только уникальные данные, которые можно использовать для анализа.
# 
# #### Для дальнейшей работы:
# * для определения зависимости целей кредита и его просрочки, нам нужно будет выделить несколько основных целей, провести лемматизацию с исходными данными таблицы и создать новый столбец с более краткими целями, по которым можно будет провести анализ.

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Работа с дубликатами - это важная часть предобработки данных. Для того, чтобы убедиться наверняка, что найденные нами дубликаты действительно таковыми являются, можно использовать метод dublicated с параметром 'keep'. Подробнее об этом ты можешь прочитать <a href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html" title="pandas documentation">здесь</a> и <a href="https://www.geeksforgeeks.org/python-pandas-dataframe-duplicated/" title="GeeksForGeeks">здесь</a>
# </div>

# <a id='Лемматизация'></a>
# ### Лемматизация

# * создадим словарь для целей кредита, столбец purpose;
# * лемматизируем исходные цели и создадим соответствующие более краткие категории, добавим новые категории в словарь с помощью метода apply();
# * добавим новый столбец в исходную табличку с данными по категориям целей кредита с помощью метода merge().

# In[21]:


#Создаем словарик
slovarik = pd.DataFrame(data = df.purpose.unique(), columns = ['purpose'])
slovarik


# ##### Итог 1.
# Нашли уникальные значения столбца с целями кредита и создали словарик

# In[22]:


#лемматизируем исходные цели и создадим соответствующие более краткие категории, добавим новые категории в словарь
from pymystem3 import Mystem
m = Mystem()
 
def purpose_category(slovarik):
   
    lemmas = m.lemmatize(slovarik)
    
    if ('недвижимость' in lemmas) or ('жилье' in lemmas):
        return 'недвижимость'
 
    elif 'образование' in lemmas:
        return 'образование'
 
    elif 'автомобиль' in lemmas:
        return 'автомобиль'
 
    elif 'свадьба' in lemmas:
        return 'свадьба'
    
slovarik['category'] = slovarik['purpose'].apply(purpose_category)
slovarik


# ##### Итог 2.
# 
# Получили словарик с более краткими категориями целей кредита

# In[23]:


#теперь склеим исходную табличку и полученный словарь
df=df.merge(slovarik, on='purpose', how='left')
df


# #### Вывод:
# 
# Теперь мы можем категоризировать данные по целям кредита и определить его влияние на возврат кредита в срок.
# 

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Прекрасное решение! Лемматизация - эффективный способ побороть хаос в данных😎
# </div>

# <a id='Категоризация данных'></a>
# ### Категоризация данных

# Проведем категоризацию данных:
# 
# * по ежемесячному доходу, столбец 'total_income'
# * по количеству детей, столбец 'children'
# * по количеству отработанных дней, столбец 'days_employed' - 
# * по возрасту, столбец 'dob_years'

# In[64]:


#медианное, минимальное и максимальное значения столбца total_income:
print(df['total_income'].min())
print(df['total_income'].max())
print(df['total_income'].median())


# Категоризируем столбец total_income, считая, что:
#  * клиенты, получающие до 50000 имеют низкий доход
#  * клиенты, получающие до 50000 - 150000 имеют средний доход
#  * клиенты, получающие больше 150000 имеют высокий доход

# In[65]:


def income_group(row):
    if row['total_income'] <= 50000:
        return 'низкий доход'
    elif 50000 < row['total_income'] <= 150000:
        return 'средний доход'
    else:
        return 'высокий доход'

df['income_group'] = df.apply(income_group, axis=1)
df.groupby('total_income_group')['total_income'].count()


# In[66]:


def children_group(row):
    if row['children'] < 1:
        return 'нет детей'
    elif 1 < row['children'] <= 2:
        return '1-2 ребенка'
    else:
        return 'более 2 детей'

df['children_group'] = df.apply(children_group, axis=1)
df.groupby('children_group')['children'].count()


# In[67]:


def days_employed_group(row):
    if row['days_employed'] < 3650:
        return 'до 10 лет'
    elif 3650 < row['days_employed'] <= 12775:
        return 'от 10 до 35 лет'
    else:
        return 'более 35 лет'

df['days_employed_group'] = df.apply(days_employed_group, axis=1)
df.groupby('days_employed_group')['days_employed'].count()


# In[68]:


def dob_years_group(row):
    if row['dob_years'] < 35:
        return 'молодой'
    elif 35 < row['dob_years'] <= 65:
        return 'средний возраст'
    else:
        return 'пожилой'

df['dob_years_group'] = df.apply(dob_years_group, axis=1)
df.groupby('dob_years_group')['dob_years'].count()


# In[69]:


#Выведем общую таблицу с категоризированными данными
df.head()


# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Здорово, что ты автоматизировала категоризацию данных. Это то, что нужно!
# </div>

# <a id='Ответы на вопросы'></a>
# ### Шаг 3. Ответьте на вопросы

# - Есть ли зависимость между наличием детей и возвратом кредита в срок?

# In[54]:


df.pivot_table(index='children_group',values='debt',aggfunc=['mean','count'])


# ##### Итог 1.
# В семьях с детьми вероятность просрочки выше

# - Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[55]:


df.pivot_table(index='family_status',values='debt',aggfunc=['mean','count'])


# ##### Итог 2.
# 
# У тех клиентов, кто был желан/замужем или находится в данном статусе, вероятность просрочки меньше, чем у тех, кто официально не узаконил свои отношения.

# - Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# In[56]:


df.pivot_table(index='income_group',values='debt',aggfunc=['mean','count'])


# ##### Итог 3.
# 
# Можно было бы предположить, что у людей с большим количеством дохода вероятность просрочки должна быть самая низкая, но результаты исследования показывают, что наименьшая вероятность просрочки у клиентов с низким доходом.

# - Как разные цели кредита влияют на его возврат в срок?

# In[57]:


df.pivot_table(index='category',values='debt',aggfunc=['mean','count'])


# #### Итог 4: 
# Выдача кредита на категории "свадьба" и "недвижимость" имеют меньшьшую вероятность просрочки по срокам, нежели категории "образование" и "автомобиль". Возможно, такие результаты исследования подтверждают исследования зависимости возврата кредита в срок и семейного положения. 

# <div class="alert alert-success">
# <h2> Комментарий ревьюера</h2>
# 
# <b>Все отлично!👍:</b> Интересные выводы! Также для того, чтобы ответить на поставленные вопросы, можно было использовать метод corr(), который расчитывает корреляцию между признаками и визуализировать результаты с помощью типа графика heatmap (коррелограмма)
# </div>

# <a id='Общий вывод'></a>
# ## Общий вывод:
# 
# Отвечая на вопрос задания "влияет ли семейное положение и количество детей клиента на факт погашения кредита в срок" - да, клиенты в браке и без детей - самые благоприятные заемщики.
# 
# По результатам проведенного исследования можно сделать вывод, что:
# * самые надежные креднитные заемщики - это клиенты с узаконенныи отношениями, без детей, с целью кредита - недвижимость или свадьба. А вот высокий уровень дохода не повышает вероятность возврата кредита в срок.
# * неблагоприятные заемщики - это клиенты банка, которые не находятся в браке, с несколькими детьми, берущие кредит на автомобиль или образование.
# 

# ### <font color='blue'>Общий вывод по проекту</font>
# Поздравляю с окончанием проекта! Ты проделала сложную работу и справилась с ней очень хорошо! Твой проект принят, и ты можешь перейти на следующий этап! 
# Отмечу некоторые положительные моменты проекта дополнительно🙂:
# * Хотелось бы отметить аккуратность ведения кода: очень здорово, что ты уделила время оформлению своей работы, использовала Markdown, ссылки и заголовки. Твою работу было приятно читать и проверять!
# * Отдельный плюс - это автоматизация решений некоторых разделов проекта. У тебя получились очень эффективные решения с помощью функций и циклов;
# * Ты провела корректную работу с пропущенными и аномальными значениями - продолжай в том же духе!
# * Отдельно хочу отметить твое внимание к промежуточным и итоговым выводам по задачам и отдельным шагам: они сформулированы подробно и основательно! Не теряй эту практику и применяй ее в своих следующих проектах!

# ### Чек-лист готовности проекта
# 
# Поставьте 'x' в выполненных пунктах. Далее нажмите Shift+Enter.

# - [x]  открыт файл;
# - [x]  файл изучен;
# - [x]  определены пропущенные значения;
# - [x]  заполнены пропущенные значения;
# - [x]  есть пояснение, какие пропущенные значения обнаружены;
# - [x]  описаны возможные причины появления пропусков в данных;
# - [x]  объяснено, по какому принципу заполнены пропуски;
# - [x]  заменен вещественный тип данных на целочисленный;
# - [x]  есть пояснение, какой метод используется для изменения типа данных и почему;
# - [x]  удалены дубликаты;
# - [x]  есть пояснение, какой метод используется для поиска и удаления дубликатов;
# - [x]  описаны возможные причины появления дубликатов в данных;
# - [x]  выделены леммы в значениях столбца с целями получения кредита;
# - [x]  описан процесс лемматизации;
# - [x]  данные категоризированы;
# - [x]  есть объяснение принципа категоризации данных;
# - [x]  есть ответ на вопрос: "Есть ли зависимость между наличием детей и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Есть ли зависимость между семейным положением и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Есть ли зависимость между уровнем дохода и возвратом кредита в срок?";
# - [x]  есть ответ на вопрос: "Как разные цели кредита влияют на его возврат в срок?";
# - [x]  в каждом этапе есть выводы;
# - [x]  есть общий вывод.
