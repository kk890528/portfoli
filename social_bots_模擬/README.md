# 論文 Cheng, Chun, Yun Luo, and Changbin Yu. "Dynamic mechanism of social bots interfering with public opinion in network." Physica A: statistical mechanics and its applications 551 (2020): 124163. 論文模擬

### 檔案social_bots為模型的程式，run_the_model為執行和畫圖的程式，另附上模擬成果


### 論文簡介
本為目的：在沉默螺旋理論下建立一個模型基於個人互動解釋能bots影響公眾與論。
模型設置與參數 ：
1. Agents：human and bots (N=1000, bots數量可控)
2.  Opinion ： 正面或負面(離散)，且不會改變
3.  Opinion Climate： 輿論風向，sigmoid function 表示，影響因素為網絡鄰軍的意見。
4.  發言的慾望： 人們發言的慾望，會受到輿論風向改變，初始為U(0,1)
5.  發言門檻：慾望超過這個數值就會方言，反之則否，且其不變，設置為U(0,1)
Bots特性：皆負面意見，且無論風向如何都會發言，不會輿論被影響，目的為主宰風向
網絡：WS network

### 模擬步驟
Step1 : 設置初始參數與網絡  n/
Step2：依照當前狀況，計算出每個Agents所屬位置的Opinion Climate /n
Step3：算出每位行動者的發表意願，且如果＞標準便會發言 /n
Step4：回到Step2 重複模擬，當穩定時，如果發言的人裡面，負面發言占了超過2/3，便算AI主宰輿論 /n
