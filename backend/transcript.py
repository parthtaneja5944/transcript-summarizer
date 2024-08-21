from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from flask import jsonify, request
from transformers import pipeline

# Initialize the summarization pipeline outside the function for efficiency
summarization = pipeline("summarization")

def summarize(original_text):
    try:
        summary_text = summarization(original_text)[0]['summary_text']
        return summary_text
    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return "Summarization failed."

def get_transcript_english(video_id):
    try:
        # Fetch the list of transcripts for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = [transcript.language_code for transcript in transcript_list]
        print(f"Available languages: {available_languages}")

        if not available_languages:
            return "No transcripts are available"

        # Check if English transcript is available
        if 'en' in available_languages:
            english_transcript = transcript_list.find_transcript(['en'])
            return english_transcript.fetch()

        # Attempt translation if English transcript is not found
        available_transcript = transcript_list.find_transcript(available_languages)
        if available_transcript.is_translatable:
            translated_transcript = available_transcript.translate('en').fetch()
            return translated_transcript
        else:
            return available_transcript.fetch()

    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"Transcript error: {str(e)}")
        return f"Error fetching transcript: {str(e)}"
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return "An unexpected error occurred."

def youtube_transcript(request):
    try:
        video_id = request.args.get('video_id')
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        transcript = get_transcript_english(video_id)
        if isinstance(transcript, str):  # Error or message string
            return jsonify({"error": transcript}), 404

        full_transcript = " ".join([segment['text'] for segment in transcript])
        print(f"Full transcript: {full_transcript}")

        summarized_text = summarize(full_transcript)
        print(f"Summarized text: {summarized_text}")

        return jsonify({"summary": summarized_text})

    except Exception as e:
        print(f"An error occurred during request handling: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

