* [x] Basic (most important) functionality of text to morse code in CLI.
* [x] Morse code audio playing/broadcasting functionality in CLI.
    * [x] Implement custom configurations for the user:
        - speed
        - pitch (frequency)
        - volume
* > [>] Implement text to morse code feature as for web UI using NiceGUI.
* [ ] Add playing/listening morse code as audio feature in web UI.
* [ ] Functionalities & Samples:
    - https://morsecode.world/international/translator.html
    - https://blendertimer.com/web-tools/morse-code-translator
    - https://morsetranslator.net/
    - https://onlinetexttools.com/convert-text-to-morse
    - https://dnschecker.org/morse-code-translator.php

* Try these 1-no encoding & raw bytes; 2-Web Audio API approaches:

    The "Ninja" optimization for this isn't about finding a better way to encode the text—it's about **removing the encoding altogether.**

    In the web world, the most efficient way to send binary data (like your audio) is to serve it as a **Raw Binary Blob** via a dedicated endpoint. This keeps the file size 100% true to the original math and allows the browser to use its native streaming capabilities.

    Here is how you handle this in **NiceGUI/FastAPI** like a pro.

    ---

    ### The Strategy: "The On-the-Fly Endpoint"

    Instead of turning your audio into a giant string (Base64), you create a tiny, temporary "Radio Station" on your server. When the browser asks for the audio, you stream the raw bytes directly from RAM.

    ### 1. The Logic

    1. **Generate** your `numpy` audio data.
    2. **Pack** it into a `io.BytesIO` buffer (exactly as we did before).
    3. **Expose** that buffer through a FastAPI `Response` with the media type `audio/wav`.
    4. **Point** the NiceGUI `ui.audio` element to that internal URL.

    ### 2. The Implementation (Concept)

    Instead of a function that returns a string, you use **FastAPI's routing** which is already built into NiceGUI.

    ```python
    from fastapi import Response
    from nicegui import app, ui
    import io
    import wave
    import numpy as np

    # A dictionary to act as our "In-Memory" storage
    # This prevents writing to disk
    audio_cache = {}

    @app.get('/audio/{audio_id}')
    def get_audio(audio_id: str):
        # This is the 'Ninja' part: 
        # We grab the raw bytes from RAM and send them as-is
        if audio_id in audio_cache:
            return Response(content=audio_cache[audio_id], media_type="audio/wav")
        return Response(status_code=404)

    def trigger_beep():
        # 1. Generate your math (simplified here)
        # ... (Your numpy logic from before) ...
        
        # 2. Write to BytesIO
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(44100)
            # w.writeframes(...) 
        
        # 3. Store in RAM and update UI
        audio_id = "last_beep" 
        audio_cache[audio_id] = buffer.getvalue()
        
        # 4. Tell the audio element to 'hit' our new endpoint
        # We add a timestamp (?t=...) to force the browser to reload the 'new' beep
        audio_player.source = f'/audio/{audio_id}?t={np.random.random()}'
        audio_player.play()

    audio_player = ui.audio('', controls=False).classes('hidden')
    ui.button('Play Ninja Beep', on_click=trigger_beep)

    ```

    ---

    ### Why this is the Optimal Way:

    * **Size:** You save that **33% bandwidth** overhead. For a 1-second beep, it’s negligible; for a 10-second sequence, it's massive.
    * **Memory Efficiency:** The browser doesn't have to "parse" a million-character string. It just opens a data stream.
    * **Browser Caching:** By using a URL, the browser can actually cache the sound if it’s one you use frequently (like a standard "Dit"), saving even more network traffic.

    ### The Trade-off

    The only "cost" of the Ninja way is that you have to manage the `audio_cache`. If you generate thousands of unique beeps and never delete them from your dictionary, your server's RAM will eventually fill up.

    **Pro Tip:** In a real app, you’d use a `uuid` as the key and perhaps a "Least Recently Used" (LRU) cache to automatically delete old beeps.

    ---

    ### The "Hidden" 3rd Way (The True Master)

    If you want the **absolute lowest latency possible** (faster than the Ninja way), you go back to the very first thing we discussed: **The Web Audio API (Instructions, not Audio).** Sending the instructions `{"freq": 440}` is only about **20 bytes**. Sending even a tiny WAV file is usually **40,000+ bytes**.
*