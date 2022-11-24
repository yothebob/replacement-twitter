import logo from './logo.svg';
import styles from './App.module.css';

const fetchAccount = async (key) => {
    const url = "/api/Account/" + key + "/";
    const res = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }        
    });
    const json = await res.json();
    return json;
}

const account = await fetchAccount(1);

function App() {
    return (
    <div class={styles.App}>
      <div>
        <h3>{account.username}</h3>
        <div class={styles.feed}>
          <For each={account.posts}>{(post, i) =>
              <div class={styles.post}>
                <div class={styles.displaybar}>
                  <p> {account.username} </p>
                  <p> {post.title} </p>
                </div>
                <div class={styles.displayaround}>
                  {post.content}
                </div>
                <div class={styles.displaybar}>
                  <div>{post.likes.length} likes</div>
                  <div>{post.comments.length} comments</div>
                </div>
              </div>
          }</For>
        </div>
        
      </div>
    </div>
  );
}

export default App;
