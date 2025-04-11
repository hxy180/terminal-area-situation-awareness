import express from 'express';
import { exec } from 'child_process';
import cors from 'cors';

const app = express();

app.use(cors());
app.use(express.json());

app.get('/execute-command', (req, res) => {
    // 测试用 ipconfig 命令，之后可替换为 MATLAB 命令
    const command = 'ipconfig';
    
    exec(command, { encoding: 'buffer' }, (error, stdout, stderr) => {
        try {
            if (error) {
                console.error('执行错误:', error);
                return res.status(500).json({ error: error.message });
            }
            
            if (stderr && stderr.length > 0) {
                console.error('命令错误:', stderr.toString());
                return res.status(500).json({ error: stderr.toString() });
            }

            const output = stdout.toString('utf8');
            res.json({ output: output });
        } catch (e) {
            console.error('处理错误:', e);
            res.status(500).json({ error: '内部服务器错误: ' + e.message });
        }
    });
});

app.listen(3000, () => {
    console.log('服务器运行在 http://localhost:3000');
});