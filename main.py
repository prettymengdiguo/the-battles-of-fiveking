# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:29:54 2018

@author: 29407
"""

import unicodecsv
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
sns.set_style("darkgrid",{"font.sans-serif":['simhei', 'Arial']})

battles_df = pd.read_csv('battles.csv',index_col='battle_number')
battles_df.head()
battles_df.info()
battles_df.describe()
battles_df.describe(include=[np.object])
#缺失值处理
#因为观察数据可知attacker_2，3，4及defender_2，3，4，数据量极少，本次不作为主要分析对象，故删除
battles_df=battles_df.drop(['attacker_2','attacker_3','attacker_4','defender_2','defender_3','defender_4'],axis=1)
#means=battles_df.mean()
#print(means)
#battles_df.fillna(means,inplace=True)
#用众数填充分类变量
#battles_df.attacker_king.fillna('',inplace=True)
#battles_df.defender_king.fillna('',inplace=True)
#battles_df.location.fillna('Riverrun',inplace=True)
#battles_df.attacker_outcome.fillna('win',inplace=True)
#哪个国王发起战争最多/每个国王发起战争的次数

battles_df['attacker_king'].value_counts().plot(kind='bar')
plt.title('每个国王发起战争的次数')
plt.xlabel('国王名称')
plt.ylabel('发起的战争次数')
plt.show()
#Joffrey/Tommen Baratheon
#哪个区域发生战争最多
battles_df['region'].value_counts().plot(kind='bar')
plt.show()
#Riverrun
#哪种战争类型最多
battles_df['battle_type'].value_counts().plot(kind='bar')
plt.show()
#pitched_battle
#获胜次数最多的国王
battles_df2 = battles_df.loc[:,['attacker_outcome', 'attacker_king', 'defender_king']]
battles_df2['win_king'] = battles_df2.apply(lambda x: x.attacker_king \
                           if x.attacker_outcome == 'win' else x.defender_king, axis = 1)
battles_df2['win_king'].value_counts().plot(kind='bar')
plt.show()
#Joffrey/Tommen Baratheon
#各个发起战争国王的成功率
#将win替换成1，loss替换成0,缺失值剔除
#因为有空值，先把attacker_outcome为空的行去掉
battles_s_df = battles_df.dropna(subset=['attacker_outcome'])
battles_s_df['attacker_outcome'] = battles_s_df['attacker_outcome'].map({"win":1, "loss":0})
#battles_s_df = battles_s_df.replace({'win':1,'loss':0})
attacker_win = (battles_s_df.groupby(['attacker_king']).sum())['attacker_outcome']
attacker_total = (battles_s_df.groupby(['attacker_king']).count())['attacker_outcome']
attacker_success_rate = attacker_win/attacker_total
attacker_success_rate.plot(kind='bar')
plt.show()
#Balon/Euron Greyjoy成功率最高
#防御成功的概率
defender_total = (battles_s_df.groupby(['defender_king']).count())['attacker_outcome']
defender_loss = (battles_s_df.groupby(['defender_king']).sum())['attacker_outcome']
defender_win = defender_total-defender_loss
defender_win_rate = defender_win/defender_total
defender_win_rate.plot(kind='bar')
plt.show()
#Mance Rayder防御成功率最高

#获胜率
df_r = battles_df.groupby(['attacker_king','attacker_outcome']).name.count().unstack()
df_r.columns.name = None
df_r.fillna(0,inplace = True)
df_r["ratio"] = df_r["win"]/(df_r["win"]+df_r["loss"])
#绘图
ax1 = df_r[["win","loss"]].plot(kind = 'bar')
ax2 = ax1.twinx()
ax2.set_ylim(0,1.1)
ax2.plot(df_r.index,df_r["ratio"],'ro-')# ro- 是一种格式简写，r-read,o-标点，- -折线 
ax1.legend(bbox_to_anchor=(1.3, 1.03))
plt.legend(bbox_to_anchor=(1.315, 0.83))
plt.show()
#战争的结果与攻击力量的相关性
#剔除异常值
battles_s_df = battles_s_df[battles_s_df['attacker_size']<100000]
battles_outcome_size=battles_s_df[['attacker_outcome','attacker_size']]
battles_outcome_size.corr()
#战争的胜利与攻击力量成中等相关
#战争的胜利是否与攻击力量和防御力量的差值相关
battles_ss_df = pd.DataFrame(battles_s_df,columns=['attacker_outcome','cha'])
battles_ss_df['cha'] = battles_s_df['attacker_size']-battles_s_df['defender_size']
battles_ss_df.corr()
#战争的胜利与攻击力量和防御力量的差值成中等相关