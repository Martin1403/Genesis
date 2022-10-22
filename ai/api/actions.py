from functools import wraps
import pickle

from ai.api.model import Seq2SeqModel, tf

tf.reset_default_graph()
word2id = pickle.load(open("ai/model/word2id.pkl", "rb"))
id2word = pickle.load(open("ai/model/id2word.pkl", "rb"))
args = pickle.load(open(f"ai/model/args.pkl", "rb"))

model = Seq2SeqModel(10, word2id, id2word, args.maxlen)
model.declare_placeholders()
model.create_embeddings(args.emb)
model.build_encoder(args.hidden)
model.memory_network(args.hidden)
model.build_decoder(args.hidden, len(word2id.keys()), word2id['^'], word2id['$'])

session = tf.compat.v1.Session()
session.run(tf.compat.v1.global_variables_initializer())
saver = tf.compat.v1.train.Saver()
saver.restore(session, f"ai/model/model.ckpt")


def action_endpoint(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        data = await f(*args, **kwargs)
        # model.empty_memory(10)
        data = model.predict_sentence(data.data, session)
        return {"data": data}
    return decorated_function
