from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, TimeDistributed, Dense
def build_model(num_tags, numwords, hidden_size=50, max_len=75, embedding=40):
    # Model architecture
    input = Input(shape=(max_len,))
    model = Embedding(input_dim=numwords, output_dim=embedding, input_length=max_len, mask_zero=False)(input)
    model = Bidirectional(LSTM(units=hidden_size, return_sequences=True, recurrent_dropout=0.1))(model)
    model = Bidirectional(LSTM(units=hidden_size, return_sequences=True, recurrent_dropout=0.1),
                          merge_mode='concat')(
        model)
    out = TimeDistributed(Dense(num_tags + 1, activation="softmax"))(model)
    # crf = CRF(num_tags + 1)  # CRF layer
    # out = crf(model)  # output

    model = Model(input, out)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    # model.summary()
    return model
