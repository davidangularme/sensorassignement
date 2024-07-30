import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:html';

class SubmitGrade extends StatefulWidget {
  @override
  _SubmitGradeState createState() => _SubmitGradeState();
}

class _SubmitGradeState extends State<SubmitGrade> {
  final _formKey = GlobalKey<FormState>();
  String _studentId = '';
  String _subject = '';
  int _grade = 0;

  Future<void> _submitGrade() async {
    final response = await http.post(
      Uri.parse('/grades'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'student_id': _studentId,
        'subject': _subject,
        'grade': _grade,
      }),
    );

    if (response.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Grade submitted successfully')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to submit grade')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Submit Grade'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: <Widget>[
              TextFormField(
                decoration: InputDecoration(labelText: 'Student ID'),
                onChanged: (value) {
                  setState(() {
                    _studentId = value;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a student ID';
                  }
                  return null;
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Subject'),
                onChanged: (value) {
                  setState(() {
                    _subject = value;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a subject';
                  }
                  return null;
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Grade'),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _grade = int.parse(value);
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a grade';
                  }
                  final grade = int.tryParse(value);
                  if (grade == null || grade < 0 || grade > 100) {
                    return 'Please enter a valid grade between 0 and 100';
                  }
                  return null;
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _submitGrade();
                  }
                },
                child: Text('Submit Grade'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
