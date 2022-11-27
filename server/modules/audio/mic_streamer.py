from flask import Flask, Response, request, render_template
import requests
import pyaudio

def start_server(port=9103):
    app = Flask(__name__, template_folder='./')


    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024

    
    audio = pyaudio.PyAudio()
    


    def genHeader(sampleRate, bitsPerSample, channels):
        datasize = 2000*10**6
        o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
        o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
        o += bytes("WAVE",'ascii')                                              # (4byte) File type
        o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
        o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
        o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
        o += (channels).to_bytes(2,'little')                                    # (2byte)
        o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
        o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
        o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
        o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
        o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
        o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
        return o

    @app.route('/audio')
    def audioRoute():
        # start Recording
        def sound():

            CHUNK = 1024
            sampleRate = RATE
            bitsPerSample = 16
            channels = CHANNELS
            wav_header = genHeader(sampleRate, bitsPerSample, channels)

            stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
            print("recording...")
            #frames = []
            first_run = True
            while True:
                if first_run:
                    data = wav_header + stream.read(CHUNK)
                    first_run = False
                else:
                    data = stream.read(CHUNK)
                yield(data)

        return Response(sound(), mimetype="audio/x-wav;codec=pcm")
    
    print("Starting mic server")
    app.run(host='0.0.0.0', debug=True, use_reloader=False, threaded=True,port=port)
