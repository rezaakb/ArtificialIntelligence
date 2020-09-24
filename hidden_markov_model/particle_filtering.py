import random

import numpy as np
import time
ee = time.perf_counter()

a = input().split()
n = int(a[0])
m = int(a[1])
mu = np.zeros(n)
sigma = np.zeros(n)
r = np.zeros(n)
thetha = np.zeros(n)
angle = np.zeros(n)
for i in range(n):
    a = input().split()
    mu[i] =float(a[0])
    sigma[i] =float(a[1])
    r[i] =float(a[2])
    thetha[i] =float(a[3])
    angle[i] =float(a[4])

dis = np.zeros((60*m,n))
landa = np.zeros(60*m)

for i in range(60* m):
    a = list(map(float,input().split()))
    dis[i,:]= a[0:n]
    landa[:]=a[n]


def findCordinateXYZ(r, thetha, angle):
    tmp_a = (thetha/180)*np.pi
    tmp_b = (angle/180)*np.pi
    tmp1 = np.sin(tmp_a)
    tmp2 = np.cos(tmp_a)
    tmp3 = np.sin(tmp_b)
    tmp4 = np.cos(tmp_b)
    x = tmp2*r*tmp4
    y = tmp1*r*tmp4
    z = tmp3*r
    return x,y,z

def findCordinateParticles(particles):
    return findCordinateXYZ(6371,particles[:,0],particles[:,1])

def findNewAngle(cos_landa):
    return  (np.arcsin((cos_landa/2)/6371)/(np.pi))*180


def moveParticles(particles, landa_tmp):
    landa_2 = np.random.exponential(scale=landa_tmp, size=(1,len(particles)))
    cos_landa = np.random.rand(1,len(particles))*2-1
    sin_landa = np.sqrt(1-cos_landa**2) * landa_2
    cos_landa = cos_landa*landa_2
    tmp = np.random.rand(1, len(particles))
    sin_landa[tmp>0.5] = -1 * sin_landa[tmp>0.5]
    particles[:, 0] =  (np.arcsin((cos_landa/2)/6371)/(np.pi))*360 + particles[:, 0]
    particles[:, 1] =  (np.arcsin((sin_landa/2)/6371)/(np.pi))*360+ +particles[:, 1]
    particles = particles%360

    '''
    landa_2 = np.random.exponential(scale=landa_tmp, size=(1,len(particles)))
    za = np.random.random(num)*2*np.pi
    particles[:, 0] = landa_2*np.sin(za)+ particles[:, 0]
    particles[:, 1] =  landa_2*np.cos(za)+ +particles[:, 1]
    particles = particles%360
    '''
    return particles

def resample(weights, particles,i):
    new_weights = (weights-np.min(weights))/(np.max(weights)-np.min(weights))
    new_weights = new_weights/np.sum(new_weights)
    w = np.random.choice(range(len(weights)), num, p=new_weights)
    new_particles = particles[w]
    weights = weights[w]
    return new_particles,weights


def findDistances(particles,weights,dis):
    x2, y2, z2 = findCordinateParticles(particles)
    tmp=np.zeros((n,num))
    for i in range(n):
        tmp[i] = np.sqrt((x1[i]-x2)**2+(y1[i]-y2)**2+(z1[i]-z2)**2)-dis[i]
        #tmp[i] = np.exp(- ((mu[i] - tmp[i]) ** 2) / (sigma[i] ** 2) / 2.0) / np.sqrt(2.0 * np.pi * (sigma[i] ** 2))
        tmp[i] = -(tmp[i] - mu[i]) ** 2 / (2 * (sigma[i] ** 2))-np.log(sigma[i]*np.sqrt(np.pi*2))
    weights= weights + np.sum(tmp,axis=0)
    return weights


num = 8500
x1, y1, z1 = findCordinateXYZ(r, thetha, angle)

w=0
particles=np.random.random((num,2))*360


weights = findDistances(particles,np.zeros(num),dis[i])

for i in range(60*m):
    particles = moveParticles(particles,landa[i])
    weights = findDistances(particles,weights,dis[i])
    particles,weights = resample(weights,particles,i)

print(particles[np.argmax(weights), 0], particles[np.argmax(weights), 1])
