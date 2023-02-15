from flask import Flask, render_template, request, flash
import hashlib

app = Flask(__name__)
app.secret_key = "blockchain"

class Block:
    def __init__(self, name, data, previous_hash):
        self.name = name
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.create_hash()

    def create_hash(self):
        block_header = str(self.name) + str(self.data) + str(self.previous_hash)
        block_hash = hashlib.sha256(block_header.encode()).hexdigest()
        return block_hash

class Blockchain:
    def __init__(self):
        self.blockchain = [Block("Genesis Block", "This is the first block", "0")]

    def add_block(self, name, data):
        previous_hash = self.blockchain[-1].hash
        new_block = Block(name, data, previous_hash)
        self.blockchain.append(new_block)

bc = Blockchain()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transfer_money", methods=["POST"])
def transfer_money():
    try:
        if request.method == "POST":
            name = request.form["name"]
            data = request.form["money"]
            bc.add_block(name, data)
            blocks = []
            for block in bc.blockchain:
                block_info = {
                    'Block Name':block.name,
                    'Block Data':block.data,
                    'hash':block.hash,
                    'Previous Hash':block.previous_hash
                }
                blocks.append(block_info)
            for i in blocks:
                print(i)
            flash("Money Sended Successfully!")
            return render_template("index.html")
        else:
            flash("Something Went Wrong!!")
            return render_template("index.html")
    except:
        flash("Some Error Occured!!")
        return render_template("index.html")

if __name__ == "__main__":
    app.run()