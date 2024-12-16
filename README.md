# Shape API
Allows users to draw shapes and calculate their area. The supported shapes are **rectangle**, **triangle**, and **diamond**. The application also includes basic authentication for API access.

---

## Requirements
- **Python 3.11.9**

### Install Dependencies
Install the necessary Python packages using `pip`:

```bash
pip install fastapi==0.115.6 requests==2.32.3 pytest==8.3.4
```

---


## Running the API
To run the FastAPI application, use the following command:

```bash
python main.py
```

The server will be available at:

```
http://127.0.0.1:8000
```

---

## Running the Tests
To run the test suite, execute:

```bash
pytest test_main.py
```

---

## API Usage

### Endpoint

**URL**:  
```
POST /shape/{shape}?times={number}
```

**Authentication**:  
Basic Auth (`username`: `user`, `password`: `pass`)

### Example cURL Command

```bash
curl -X POST -u user:pass "http://127.0.0.1:8000/shape/triangle?times=3"
```

### Example Response

```json
{
  "shape": "triangle",
  "times": 3,
  "area": 6.0
}
```

---

## Supported Shapes

- **rectangle**
- **triangle**
- **diamond**

---

