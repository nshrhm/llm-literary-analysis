# Uploads
Allows you to upload large files in multiple parts.

## 1. Create upload
post https://api.openai.com/v1/uploads
Creates an intermediate Upload object that you can add Parts to. Currently, an Upload can accept at most 8 GB in total and expires after an hour after you create it.

Once you complete the Upload, we will create a File object that contains all the parts you uploaded. This File is usable in the rest of our platform as a regular File object.

For certain purpose values, the correct mime_type must be specified. Please refer to documentation for the supported MIME types for your use case.

For guidance on the proper filename extensions for each purpose, please follow the documentation on creating a File.

### Request body
bytes integer Required
The number of bytes in the file you are uploading.

filename string Required
The name of the file to upload.

mime_type string Required
The MIME type of the file.

This must fall within the supported MIME types for your file purpose. See the supported MIME types for assistants and vision.

purpose string Required
The intended purpose of the uploaded file.
See the documentation on File purposes.

Returns
The Upload object with status pending.

### Example request
```curl
curl https://api.openai.com/v1/uploads \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "purpose": "fine-tune",
    "filename": "training_examples.jsonl",
    "bytes": 2147483648,
    "mime_type": "text/jsonl"
  }'
```

### Example response
```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 2147483648,
  "created_at": 1719184911,
  "filename": "training_examples.jsonl",
  "purpose": "fine-tune",
  "status": "pending",
  "expires_at": 1719127296
}
```

## 2. Add upload part
post https://api.openai.com/v1/uploads/{upload_id}/parts
Adds a Part to an Upload object. A Part represents a chunk of bytes from the file you are trying to upload.
Each Part can be at most 64 MB, and you can add Parts until you hit the Upload maximum of 8 GB.
It is possible to add multiple Parts in parallel. You can decide the intended order of the Parts when you complete the Upload.

Path parameters upload_id string Required
The ID of the Upload.

Request body data file Required
The chunk of bytes for this Part.

Returns
The upload Part object.

### Example request
```curl
curl https://api.openai.com/v1/uploads/upload_abc123/parts
  -F data="aHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MS91cGxvYWRz..."
```

### Example response
```json
{
  "id": "part_def456",
  "object": "upload.part",
  "created_at": 1719185911,
  "upload_id": "upload_abc123"
}
```

## 3. Complete upload
post https://api.openai.com/v1/uploads/{upload_id}/complete
Completes the Upload.
Within the returned Upload object, there is a nested File object that is ready to use in the rest of the platform.
You can specify the order of the Parts by passing in an ordered list of the Part IDs.
The number of bytes uploaded upon completion must match the number of bytes initially specified when creating the Upload object. No Parts may be added after an Upload is completed.

Path parameters upload_id string Required
The ID of the Upload.

Request body part_ids array Required
The ordered list of Part IDs.

md5 string Optional
The optional md5 checksum for the file contents to verify if the bytes uploaded matches what you expect.

Returns
The Upload object with status completed with an additional file property containing the created usable File object.

### Example request
```curl
curl https://api.openai.com/v1/uploads/upload_abc123/complete
  -d '{
    "part_ids": ["part_def456", "part_ghi789"]
  }'
```

### Example response
```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 2147483648,
  "created_at": 1719184911,
  "filename": "training_examples.jsonl",
  "purpose": "fine-tune",
  "status": "completed",
  "expires_at": 1719127296,
  "file": {
    "id": "file-xyz321",
    "object": "file",
    "bytes": 2147483648,
    "created_at": 1719186911,
    "filename": "training_examples.jsonl",
    "purpose": "fine-tune",
  }
}
```

## 4. Cancel upload
post https://api.openai.com/v1/uploads/{upload_id}/cancel
Cancels the Upload. No Parts may be added after an Upload is cancelled.

### Path parameters
upload_id string Required
The ID of the Upload.

Returns
The Upload object with status cancelled.

### Example request
```curl
curl https://api.openai.com/v1/uploads/upload_abc123/cancel
```

### Example response
```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 2147483648,
  "created_at": 1719184911,
  "filename": "training_examples.jsonl",
  "purpose": "fine-tune",
  "status": "cancelled",
  "expires_at": 1719127296
}
```

## 5. The upload object
The Upload object can accept byte chunks in the form of Parts.
bytes integer
The intended number of bytes to be uploaded.

created_at integer
The Unix timestamp (in seconds) for when the Upload was created.

expires_at integer
The Unix timestamp (in seconds) for when the Upload will expire.

file undefined or null
The ready File object after the Upload is completed.

filename string
The name of the file to be uploaded.

id string
The Upload unique identifier, which can be referenced in API endpoints.

object string
The object type, which is always "upload".

purpose string
The intended purpose of the file. Please refer here for acceptable values.

status string
The status of the Upload.

```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 2147483648,
  "created_at": 1719184911,
  "filename": "training_examples.jsonl",
  "purpose": "fine-tune",
  "status": "completed",
  "expires_at": 1719127296,
  "file": {
    "id": "file-xyz321",
    "object": "file",
    "bytes": 2147483648,
    "created_at": 1719186911,
    "filename": "training_examples.jsonl",
    "purpose": "fine-tune",
  }
}
```

## 6. The upload part object
The upload Part represents a chunk of bytes we can add to an Upload object.

created_at integer
The Unix timestamp (in seconds) for when the Part was created.

id string
The upload Part unique identifier, which can be referenced in API endpoints.

object string
The object type, which is always upload.part.

upload_id string
The ID of the Upload object that this Part was added to.

```json
{
    "id": "part_def456",
    "object": "upload.part",
    "created_at": 1719186911,
    "upload_id": "upload_abc123"
}
```