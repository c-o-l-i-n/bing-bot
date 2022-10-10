import logging
import os
import requests
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


CLARIFAI_PERSONAL_ACCESS_TOKEN = os.environ['CLARIFAI_PERSONAL_ACCESS_TOKEN']
OPEN_EMOJI_API_KEY = os.environ['OPEN_EMOJI_API_KEY']


def identify_image(image_url: str) -> str:
  logging.info('Setting up secure channel to Clarifai')
  channel = ClarifaiChannel.get_grpc_channel()
  stub = service_pb2_grpc.V2Stub(channel)

  logging.info(f'Sending image {image_url} to Clarifai for indentification')
  response = stub.PostModelOutputs(
      service_pb2.PostModelOutputsRequest(
          user_app_id=resources_pb2.UserAppIDSet(user_id='bing-bot', app_id='b1dd02f5f09044ee9054a9d3f0ed3b31'),
          model_id='general-image-recognition',
          inputs=[
              resources_pb2.Input(
                  data=resources_pb2.Data(
                      image=resources_pb2.Image(
                          url=image_url
                      )
                  )
              )
          ]
      ),
      metadata=(('authorization', 'Key ' + CLARIFAI_PERSONAL_ACCESS_TOKEN),)
  )
  if response.status.code != status_code_pb2.SUCCESS:
      logging.error(response.status)
      return 'idk'

  cop_out_concepts = set(['illustration', 'sketch', 'art', 'vector', 'graphic', 'collection'])

  # make sure result isn't a cop out
  i = 0
  name = response.outputs[0].data.concepts[i].name
  confidence = response.outputs[0].data.concepts[i].value
  while name in cop_out_concepts:
    i += 1
    name = response.outputs[0].data.concepts[i].name
    confidence = response.outputs[0].data.concepts[i].value

  logging.info(f'Success! Top result: "{name}", confidence:  {(confidence * 100):.2f}%')

  rt = name.lower()

  # add ? if less than 99% sure
  if confidence < 0.99:
    logging.info('Adding question mark since confidence is less than 99%')
    rt += '?'

  logging.info(f'Searching emoji database for "{name}"')
  emoji_search_results = requests.get(f'https://emoji-api.com/emojis', params={'search': name, 'access_key': OPEN_EMOJI_API_KEY}).json()

  if emoji_search_results:
    logging.info(f'Found {len(emoji_search_results)} emojis')
    emoji_exact_match = next(filter(lambda e: e['unicodeName'] == name, emoji_search_results), None)
    rt += ' '
    if emoji_exact_match:
      logging.info(f'Found an exact match for "{name}" emoji')
      rt += emoji_exact_match['character']
    else:
      top_emoji_result = emoji_search_results[0]
      logging.info(f"Top result: \"{top_emoji_result['unicodeName']}\"")
      rt += top_emoji_result['character']
  else:
    logging.info('No emojis found')
  
  logging.info(f'Final result: "{rt}"')
  return rt
