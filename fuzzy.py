import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fz
import time

plt.close()
uart = serial.Serial('COM6', 115200) 
time.sleep(2.0)
#flg_ctl = str.encode('k')

''' Universos del discurso de las variables '''
U = np.arange(-47, 47.1, 0.1)  #-50 , 50 → incrementos de .1
V = np.arange(-30, 30.1, 0.1)  
W = np.arange(0, 180.1, 0.1)

''' Términos y funciones de pertenencia: error '''
etmmn = fz.trapmf(U, [-47, -47, -40, -30])
etmn = fz.trimf(U, [-35, -20, -15])
etne = fz.trapmf(U, [-25, -17, -10, 1])
etze = fz.trapmf(U, [0, 0.8, 1, 1.5])
etpo = fz.trapmf(U, [1.6, 9, 14, 20])
etmp = fz.trimf(U, [15, 25, 35])
etmmp = fz.trapmf(U, [30, 40, 47, 47])

''' Términos y funciones de pertenencia: derivada del error '''
dmn = fz.trapmf(V, [-30, -30, -25, -15])
dne = fz.trimf(V, [-20, -10, -2])
dze = fz.trapmf(V, [-5., -0.5, 0.5, 5.])
dpo = fz.trimf(V, [1, 10, 20])
dmp = fz.trapmf(V, [15, 25, 30, 30])

''' Términos y funciones de pertenencia: PWM '''
agmmb = fz.trapmf(W, [0, 0, 10, 20])
agmb = fz.trimf(W , [15, 22, 30])
agb = fz.trapmf(W, [25, 35, 40, 60])
agme = fz.trapmf(W, [55, 70, 80, 95])
aga = fz.trimf(W, [82, 97, 115])
agma = fz.trapmf(W, [90, 110, 130, 145])
agmma = fz.trapmf(W, [140, 160, 180, 180])

'''----------graficacion universos----------'''
fig, axs = plt.subplots(3)
axs[0].plot(U, etmmn, U, etmn, U, etne, U, etze, U, etpo, U, etmp, U, etmmp)
axs[0].set_title('MF: error')
axs[1].plot(V, dmn, V, dne, V, dze, V, dpo, V, dmp)
axs[1].set_title('MF: derivada del error')
axs[2].plot(W, agmmb, W, agmb, W, agb, W, agme, W, aga, W, agma, W, agmma)
axs[2].set_title('MF: angulo out')
plt.show()

'''----------crear listas para almacenar datos----------'''
xdat = []
rdat = []
tdat = []

r = float(input("ingrese set-point: "))
e_1 = 0
i = 0
ang_0 = 180

plt.figure(figsize=(10,7))
plt.ion() # Enable interactive mode 
plt.show()
# Main loop 


while (True):
    if r<25:
        r=25
    elif r>75:
        r=75
   
    Tm = float(uart.readline())
    # error 
    e = r - Tm 
    # derivada del error 
    de = (e - e_1)
    e_1 = e
    
    '''----- datos para graficar on-line -----'''
    tdat.append(Tm)
    xdat.append(i)
    rdat.append(r)
    i = i + 1
    
    '''---------- Fuzificación de e -----------'''
    u_etmmn = fz.interp_membership(U, etmmn, e)
    u_etmn = fz.interp_membership(U, etmn, e)
    u_etne = fz.interp_membership(U, etne, e)
    u_etze = fz.interp_membership(U, etze, e)
    u_etpo = fz.interp_membership(U, etpo, e)
    u_etmp = fz.interp_membership(U, etmp, e)
    u_etmmp = fz.interp_membership(U, etmmp, e)
    '''---------- Fuzificación de de -----------'''
    u_dmn = fz.interp_membership(V, dmn, de)
    u_dne = fz.interp_membership(V, dne, de)
    u_dze = fz.interp_membership(V, dze, de)
    u_dpo = fz.interp_membership(V, dpo, de)
    u_dmp = fz.interp_membership(V, dmp, de)
    '''---------- Implicación ----------'''
    impl_R1 = np.fmin(np.fmin(u_etmmn, u_dmn), agmma)  # R1
    impl_R2 = np.fmin(np.fmin(u_etmmn, u_dne), agmma)
    impl_R3 = np.fmin(np.fmin(u_etmmn, u_dze), agmma)
    impl_R4 = np.fmin(np.fmin(u_etmmn, u_dpo), agma)
    impl_R5 = np.fmin(np.fmin(u_etmmn, u_dmp), aga)
    
    impl_R6 = np.fmin(np.fmin(u_etmn, u_dmn), agma)
    impl_R7 = np.fmin(np.fmin(u_etmn, u_dne), agmma)
    impl_R8 = np.fmin(np.fmin(u_etmn, u_dze), agmma)
    impl_R9 = np.fmin(np.fmin(u_etmn, u_dpo), agma)
    impl_R10 = np.fmin(np.fmin(u_etmn, u_dmp), agma)
    
    impl_R11 = np.fmin(np.fmin(u_etne, u_dmn), agmma)
    impl_R12 = np.fmin(np.fmin(u_etne, u_dne), agmma)
    impl_R13 = np.fmin(np.fmin(u_etne, u_dze), agmma)
    impl_R14 = np.fmin(np.fmin(u_etne, u_dpo), aga)
    impl_R15 = np.fmin(np.fmin(u_etne, u_dmp), agma)
    
    impl_R16 = np.fmin(np.fmin(u_etze, u_dmn), agme)
    impl_R17 = np.fmin(np.fmin(u_etze, u_dne), agmma)
    impl_R18 = np.fmin(np.fmin(u_etze, u_dze), agma)
    impl_R19 = np.fmin(np.fmin(u_etze, u_dpo), agme)
    impl_R20 = np.fmin(np.fmin(u_etze, u_dmp), agb)
    
    impl_R21 = np.fmin(np.fmin(u_etpo, u_dmn), agb)
    impl_R22 = np.fmin(np.fmin(u_etpo, u_dne), agb)
    impl_R23 = np.fmin(np.fmin(u_etpo, u_dze), agmb)
    impl_R24 = np.fmin(np.fmin(u_etpo, u_dpo), agb)
    impl_R25 = np.fmin(np.fmin(u_etpo, u_dmp), agb)
    
    impl_R26 = np.fmin(np.fmin(u_etmp, u_dmn), agmb)
    impl_R27 = np.fmin(np.fmin(u_etmp, u_dne), agmb)
    impl_R28 = np.fmin(np.fmin(u_etmp, u_dze), agmb)
    impl_R29 = np.fmin(np.fmin(u_etmp, u_dpo), agb)
    impl_R30 = np.fmin(np.fmin(u_etmp, u_dmp), agb)
    
    impl_R31 = np.fmin(np.fmin(u_etmmp, u_dmn), agmmb)
    impl_R32 = np.fmin(np.fmin(u_etmmp, u_dne), agmmb)
    impl_R33 = np.fmin(np.fmin(u_etmmp, u_dze), agmb)
    impl_R34 = np.fmin(np.fmin(u_etmmp, u_dpo), agb)
    impl_R35 = np.fmin(np.fmin(u_etmmp, u_dmp), agmb)
    
    '''---------------- agregación -------------'''
    agreg_1 = np.fmax(impl_R1, impl_R2)
    agreg_2 = np.fmax(agreg_1, impl_R3)
    agreg_3 = np.fmax(agreg_2, impl_R4)
    agreg_4 = np.fmax(agreg_3, impl_R5)
    agreg_5 = np.fmax(agreg_4, impl_R6)
    agreg_6 = np.fmax(agreg_5, impl_R7)
    agreg_7 = np.fmax(agreg_6, impl_R8)
    agreg_8 = np.fmax(agreg_7, impl_R9)
    agreg_9 = np.fmax(agreg_8, impl_R10)
    agreg_10 = np.fmax(agreg_9, impl_R11)
    agreg_11 = np.fmax(agreg_10, impl_R12)
    agreg_12 = np.fmax(agreg_11, impl_R13)
    agreg_13 = np.fmax(agreg_12, impl_R14)
    agreg_14 = np.fmax(agreg_13, impl_R15)
    agreg_15 = np.fmax(agreg_14, impl_R16)
    agreg_16 = np.fmax(agreg_15, impl_R17)
    agreg_17 = np.fmax(agreg_16, impl_R18)
    agreg_18 = np.fmax(agreg_17, impl_R19)
    agreg_19 = np.fmax(agreg_18, impl_R20)
    agreg_20 = np.fmax(agreg_19, impl_R21)
    agreg_21 = np.fmax(agreg_20, impl_R22)
    agreg_22 = np.fmax(agreg_21, impl_R23)
    agreg_23 = np.fmax(agreg_22, impl_R24)
    agreg_24 = np.fmax(agreg_23, impl_R25)
    agreg_25 = np.fmax(agreg_24, impl_R26)
    agreg_26 = np.fmax(agreg_25, impl_R27)
    agreg_27 = np.fmax(agreg_26, impl_R28)
    agreg_28 = np.fmax(agreg_27, impl_R29)
    agreg_29 = np.fmax(agreg_28, impl_R30)
    agreg_30 = np.fmax(agreg_29, impl_R31)
    agreg_31 = np.fmax(agreg_30, impl_R32)
    agreg_32 = np.fmax(agreg_31, impl_R33)
    agreg_33 = np.fmax(agreg_32, impl_R34)
    agreg_total = np.fmax(agreg_33, impl_R35)  #sumatoria de todas las reglas
    angulo_fase = int(fz.defuzz(W, agreg_total, 'centroid'))
    #angulo_singleton = fz.interp_membership(W, agreg_total, angulo_fase)

    print(f'Referencia: {r:.2f} || Temperatura: {Tm:.2f} || Error: {e:.2f} || de: {de:.2f} || Angulo_fase: {angulo_fase} ')
    #angulo_fase2 = ang_0 + ( angulo_fase)
    #ang_0 = angulo_fase
    '''---------- Enviar angulo de disparo ----------'''
    #if (angulo_fase2 >= 0 and angulo_fase2 <= 180):
    uart.write(str(angulo_fase).encode()) # mando el sp 
    time.sleep(1)
    '''---------- grafica ----------'''
    plt.clf() #Clear current figure
    ax = plt.subplot(211)
    ax.grid()
    plt.plot(xdat[0:i-1], tdat[0:i-1],'-r',label=r'$T_1$ Control', linewidth = 2)
    plt.ylabel('Temperature (c)', fontsize=14)
    plt.legend(loc='best')
    
    ax = plt.subplot(211)
    ax.grid()
    plt.plot(xdat[0:i-1], rdat[0:i-1],'-g',label=r'$Referencia$', linewidth = 2)
    plt.ylabel('Temperature (°c)', fontsize=14)
    plt.xlabel('Time (s)', fontsize=14)
    plt.legend(loc='best')
    plt.draw()
    plt.pause(0.05)