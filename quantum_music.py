from qiskit import *

#build the circuit for random walk on a cube
def circ(input):
  qc = QuantumCircuit(5,3)
  for i, v in enumerate(input):
    #This encodes the output state from previous run as input in the next circuit
    if v=='1':
      qc.x(2-i)
  qc.h(3)
  qc.h(4)
  qc.cx(4, 0)
  qc.x(4)
  qc.cx(4, 1)
  qc.cx(3, 2)
  qc.ccx(4, 3, 1)
  qc.x(4)
  qc.ccx(4, 3, 0)
  qc.x(4)
  qc.ccx(4, 3, 2)
  qc.barrier(range(3))
  qc.measure([0,1,2],[0,1,2])
  return qc

from qiskit import Aer
backend_sim = Aer.get_backend('qasm_simulator')

#Initialize the first note
notes = ['001']

#Generate a sequence of 101 notes
for i in range(100):
  qc = circ(notes[i])
  job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)
  result_sim = job_sim.result()
  counts = result_sim.get_counts(qc)
  max_key = max(counts, key=counts.get)
  notes.append(max_key)

#Initialize the first rhythm
rhythm = ['000']

#Generate a sequence of 101 rhythms
for i in range(100):
  qc = circ(rhythm[i])
  job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)
  result_sim = job_sim.result()
  counts = result_sim.get_counts(qc)
  max_key = max(counts, key=counts.get)
  rhythm.append(max_key)

print(notes)
print(rhythm)

#Encoding the ouput quantum states to a particular pitch
#The numbers correspond to a MIDI frequency 
note_dic = {'000':60, '001':62, '100':64, '010':65, '011':67, '101':69, '111':71, '110':72}

#Encoding the ouput quantum states to a particular rhythmic beat
rhythm_dic = {'000':4, '001':3, '100':1, '010':2, '011':1.5, '101':0.75, '111':0.25, '110':0.5}

from midiutil import MIDIFile
track    = 0
channel  = 2
time     = 0   #time at which the note will be played
duration = 1   #The duration/beat note will be played for
tempo    = 80  #Tempo of the whole arrangement
volume   = 100

#Create a single track
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track,time, tempo)

for i in range (len(notes)):

  #Duration of the note taken from the generated rhythm sequence
  duration = rhythm_dic.get(rhythm[i])

  #Pitch of the note taken from the generated note sequence
  pitch = note_dic.get(notes[i])

  #Add the note for the current duration
  #A fifth, seventh and lower octave of the note
  MyMIDI.addNote(track, channel, pitch, time, duration, volume)
  MyMIDI.addNote(track, channel, pitch-5, time, duration, volume)
  MyMIDI.addNote(track, channel, pitch-7, time, duration, volume)
  MyMIDI.addNote(track, channel, pitch-12, time, duration, volume)
  time = duration + time + 0.25

#output the arrangement to a MIDI file
with open("/Users/amanhas/Desktop/Quantum.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
