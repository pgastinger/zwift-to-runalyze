from garmin_fit_sdk import Decoder, Stream

stream = Stream.from_file("Activity.fit")
decoder = Decoder(stream)
messages, errors = decoder.read()

print(errors)
print(messages)