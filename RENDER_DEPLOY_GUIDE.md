# Guia de Deploy no Render - Solução para erro de conexão MySQL

## Problema
O erro `(2003, "Can't connect to MySQL server on 'db'")` ocorre porque:
- Na sua máquina local, o Docker Compose usa `db` como hostname (serviço interno)
- No Render, esse hostname não existe - você precisa usar a string de conexão real da sua instância MySQL

## Solução

### 1. Criar instância MySQL no Render (se ainda não tem)
- Vá para https://dashboard.render.com
- Clique em "New +" → "MySQL"
- Configure conforme necessário
- Copie a **External Database URL** (formato: `mysql://user:password@host:port/database`)

### 2. Adicionar variáveis de ambiente no Render
1. Na dashboard do seu Web Service (backend)
2. Vá para "Environment"
3. Adicione a variável:
   ```
   DATABASE_URL=mysql://seu_usuario:sua_senha@seu_host:3306/seu_database
   ```

### 3. Configurar também as outras variáveis necessárias:
```
DATABASE_URL=mysql://user:password@host:port/database
OPENAI_API_KEY=sua_chave_openai
MY_WHATSAPP=seu_numero
REDIS_URL=redis://seu_redis_url
NOTIFICATION_WEBHOOK_URL=sua_webhook_url (opcional)
```

## Importante: String de conexão correta
A URL deve estar no formato:
```
mysql://username:password@hostname:port/database_name
```

Exemplo completo:
```
mysql://admin:MyP@ss123@mysql.c3lw8hlj.databases.render.com:3306/chatbot_db
```

## Dicas
- **Nunca** coloque caracteres especiais na senha sem URL-encode (se tiver `@`, use `%40`, etc)
- Use a "External Database URL" fornecida pelo Render, não a "Internal Database URL"
- O driver `aiomysql` na aplicação vai converter para `mysql+aiomysql` automaticamente
- Após adicionar variáveis, o Render vai fazer rebuild automaticamente

## Verificar logs
Se o erro persistir:
1. Va para "Logs" na dashboard do Render
2. Procure por `DATABASE_URL` para confirmar que a variável foi carregada
3. Verifique se a senha contém caracteres especiais que precisam de escape
